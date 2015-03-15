"""This module keeps track of devices appearing on the network."""

import collections
import logging
import os
import platform
import re
import subprocess
import time

import ipaddr
import netifaces
import pyping

from common import detector
from pi import scanning_proxy


# This regex matches the output of `ip -s neighbor list`
LINUX_RE = (r'^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) dev (\w+) (lladdr '
            r'(?P<mac>([0-9a-f]{2}[:-]){5}([0-9a-f]{2})))? (ref \d+ )?used '
            r'(\d+/\d+/\d+) probes \d+ (?P<state>[A-Z]+)')
LINUX_RE = re.compile(LINUX_RE)

# This regex matches the output of `arp -a`
MAC_RE = (r'^\? \((?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\) at '
          r'(?P<mac>([0-9a-f]{1,2}[:-]){5}([0-9a-f]{1,2})|\(incomplete\)) '
          r'on [a-z0-9]+ (ifscope )?(permanent )?\[ethernet\]$')
MAC_RE = re.compile(MAC_RE)


class NetworkMonitor(scanning_proxy.ScanningProxy):
  """Monitor devices appearing on the network."""

  def __init__(self, callback, scan_period_sec, timeout_secs):
    assert os.geteuid() == 0, \
        'You need to have root privileges to use this module.'

    self._callback = callback
    self._timeout_secs = timeout_secs
    self._ping_frequency_secs = 60

    self._hosts = collections.defaultdict(lambda: False)
    self._last_ping = collections.defaultdict(float)
    self._detectors = collections.defaultdict(detector.AccrualFailureDetector)

    # This module has to poll the network pretty
    # frequently to have a good chance of catching
    # iphones etc which sleep a lot.
    # Hence, we send edge-triggered events to the server
    # to rate limit the number of events we're sending.
    # (This also helps with latency).
    # This works in the other scanners as (a) we assume the
    # server is always there and (b) the server creates
    # instances on demand for things like wemo and hue.
    # We don't want to create instances on demand
    # (there is too much junk we can't control on most
    #  networks) - instead, the user will manually create
    # objects to represents phones coming and going.
    # Therefore, edge triggering isn't good enough
    # - the user might create the phone object after the
    # phone has been detected, and the server will miss
    # the event.  There we will also periodically send
    # a 'level-triggered' event - ie, just a list of
    # devices which are present.  But we'll do this
    # less frequently.
    self._level_event_frequency_secs = 10*60
    self._last_level_event = 0

    super(NetworkMonitor, self).__init__(scan_period_sec)

  def _ping(self, ip_address, now):
    """Ping a device, but rate limit.

    Don't ping more often than self._ping_frequency_secs.
    """
    if self._last_ping[ip_address] + self._ping_frequency_secs > now:
      return

    pyping.ping(ip_address, timeout=1, count=1)
    self._last_ping[ip_address] = now

  def ping_subnet(self, now):
    """Ping broadcase address for all interfaces."""
    if self._last_ping['SUBNET'] + self._ping_frequency_secs > now:
      return

    self._last_ping['SUBNET'] = now

    for interface in netifaces.interfaces():
      if interface.startswith('lo'):
        continue

      details = netifaces.ifaddresses(interface)
      if netifaces.AF_INET not in details:
        continue

      for detail in details[netifaces.AF_INET]:
        address = detail.get('addr', None)
        netmask = detail.get('netmask', None)
        if address is None or netmask is None:
          continue

        parsed = ipaddr.IPv4Network('%s/%s' % (address, netmask))
        logging.debug('Ping broadcast address %s', parsed.broadcast)
        pyping.ping(str(parsed.broadcast), timeout=10, count=10)

  def _arp(self):
    system = platform.system()
    if system == 'Darwin':
      process = subprocess.Popen(['arp', '-a'],
                                 stdin=None, stdout=subprocess.PIPE,
                                 stderr=None, close_fds=True)
      while True:
        line = process.stdout.readline()
        if not line:
          break

        match = MAC_RE.match(line)
        if not match:
          logging.error('Line not matched by regex: "%s"', line.strip())
          continue

        mac = match.group('mac')
        ip_address = match.group('ip')
        state = 'INVALID' if mac == '(incomplete)' else 'REACHABLE'

        yield (mac, ip_address, state)

    elif system == 'Linux':
      process = subprocess.Popen(['ip', '-s', 'neighbor', 'list'],
                                 stdin=None, stdout=subprocess.PIPE,
                                 stderr=None, close_fds=True)
      while True:
        line = process.stdout.readline()
        if not line:
          break

        match = LINUX_RE.match(line)
        if not match:
          logging.error('Line not matched by regex: "%s"', line.strip())
          continue

        mac = match.group('mac')
        ip_address = match.group('ip')
        state = match.group('state')
        yield (mac, ip_address, state)

  def _scan_once(self):
    """Scan the network for devices."""
    now = time.time()
    self.ping_subnet(now)

    # Now look at contents of arp table
    for mac, ip_address, state in self._arp():

      # ping everything in the table once a minute.
      self._ping(ip_address, now)

      if state != 'REACHABLE':
        continue

      self._detectors[mac].heartbeat(now)

    for mac, dtor in self._detectors.iteritems():
      # Has there been a state change?
      is_alive = dtor.is_alive(now)
      if is_alive == self._hosts[mac]:
        continue

      self._hosts[mac] = is_alive
      if is_alive:
        logging.info('Found new device - %s', mac)
        self._callback('network', None, {'appeared': mac})
      else:
        logging.info('Device disappeared - %s', mac)
        self._callback('network', None, {'disappeared': mac})

    # Periodically send event with list of
    # devices we can see.
    if self._last_level_event + self._level_event_frequency_secs < now:
      self._last_level_event = now
      alive = [mac for mac, dtor in self._detectors.iteritems()
               if dtor.is_alive()]
      self._callback('network', None, {'devices': alive})
