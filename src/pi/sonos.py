"""Wemo proxy code."""

import logging

import soco

from pi import scanning_proxy


class Sonos(scanning_proxy.ScanningProxy):
  """Sonos proxy object."""

  def __init__(self, refresh_period, callback):
    super(Sonos, self).__init__(refresh_period)

    self._callback = callback
    self._devices = {}

  def _scan_once(self):
    devices = list(soco.discover())

    logging.info('Found %d sonos devices.', len(devices))

    for device in devices:
      uid = device.uid
      device_exists = uid in self._devices
      self._devices[uid] = device

      details = {
          'uid': uid,
          'name': device.player_name,
      }

      if not device_exists:
        self._callback('sonos', 'sonos-%s' % uid, details)
