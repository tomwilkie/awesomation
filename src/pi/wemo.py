"""Wemo proxy code."""

import logging

import pywemo

from pi import scanning_proxy


class Wemo(scanning_proxy.ScanningProxy):
  """Hue proxy object."""

  def __init__(self, refresh_period, callback):
    super(Wemo, self).__init__(refresh_period)

    self._callback = callback
    self._devices = {}

  def _scan_once(self):
    devices = pywemo.discover_devices()

    logging.info('Found %d wemo devices.', len(devices))

    for device in devices:
      if device.serialnumber in self._devices:
        continue

      self._devices[device.serialnumber] = device

      details = {
        'serialnumber': device.serialnumber,
        'model': device.model,
        'name': device.name,
        'state': device.get_state()
      }
      logging.info(details)

      #self._callback('wemo', 'wemo-%s' % device.serialnumber, details))

  def handle_events(self, messages):
    """Handle hue events - turn it on or off."""
    for message in messages:
      command = message.pop('command')

      if command == 'light':
        self._set_light(message)
      else:
        super(Wemo, self).handle_events([message])
