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

  def __init__(self, period, timeout_secs):
    super(NetworkMonitor, self).__init__(period)
    self._timeout_secs = timeout_secs
    self._ping_frequency_secs = 60

    self._hosts = {}
    self._last_ping = collections.defaultdict(float)

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

      if state != 'REACHABLE':
        # give it a ping, so next time round
        # it might be considered reachable
        self._ping(ipaddr, now)
        continue

      if mac not in self._hosts:
        logging.info('Found new device - %s, %s, %s', ipaddr, mac, state)

      # update last seen time
      self._hosts[mac] = now

    # expire old timestamps
    for mac, timestamp in self._hosts.items():
      if timestamp + self._timeout_secs < now:
        del self._hosts[mac]
        logging.info('Device disappeared - %s', mac)
