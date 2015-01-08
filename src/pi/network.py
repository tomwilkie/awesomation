"""This module keeps track of devices appearing on the network."""

import collections
import logging
import re
import subprocess
import time

import pyping

from pi import scanning_proxy


# This regex matches the output of `ip -s neighbor list`
RE = (r'^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) dev (\w+) (lladdr '
      r'(?P<mac>([0-9a-f]{2}[:-]){5}([0-9a-f]{2})))? (ref \d+ )?used '
      r'(\d+/\d+/\d+) probes \d+ (?P<state>[A-Z]+)')
RE = re.compile(RE)


class NetworkMonitor(scanning_proxy.ScanningProxy):
  """Monitor devices appearing on the network."""

  def __init__(self, callback, scan_period_sec, timeout_secs):
    super(NetworkMonitor, self).__init__(scan_period_sec)
    self._callback = callback
    self._timeout_secs = timeout_secs
    self._ping_frequency_secs = 60

    self._hosts = {}
    self._last_ping = collections.defaultdict(float)

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

  def _ping(self, ipaddr, now):
    """Ping a device, but rate limit.

    Don't ping more often than self._ping_frequency_secs.
    """
    if self._last_ping[ipaddr] + self._ping_frequency_secs > now:
      return

    pyping.ping(ipaddr, timeout=1, count=1)
    self._last_ping[ipaddr] = now

  def _scan_once(self):
    """Scan the network for devices."""

    # TODO: probably need to ping the subnet?

    now = time.time()
    process = subprocess.Popen(['ip', '-s', 'neighbor', 'list'],
                               stdin=None, stdout=subprocess.PIPE,
                               stderr=None, close_fds=True)
    while True:
      line = process.stdout.readline()
      if not line:
        break

      match = RE.match(line)
      if not match:
        logging.error('Line not matched by regex: "%s"', line.strip())
        continue

      mac = match.group('mac')
      ipaddr = match.group('ip')
      state = match.group('state')

      # ping everything in the table once a minute.
      self._ping(ipaddr, now)

      if state != 'REACHABLE':
        continue

      if mac not in self._hosts:
        logging.info('Found new device - %s, %s, %s', ipaddr, mac, state)
        self._callback('network', None, {'appeared': mac})

      # update last seen time
      self._hosts[mac] = now

    # Expire old timestamps
    for mac, timestamp in self._hosts.items():
      if timestamp + self._timeout_secs < now:
        del self._hosts[mac]
        logging.info('Device disappeared - %s', mac)
        self._callback('network', None, {'disappeared': mac})

    # Periodically send event with list of
    # devices we can see.
    if self._last_level_event + self._level_event_frequency_secs < now:
      self._last_level_event = now
      self._callback('network', None, {'devices': self._hosts.keys()})
