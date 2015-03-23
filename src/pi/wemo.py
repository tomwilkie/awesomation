"""Wemo proxy code."""

import logging

import pywemo

from pi import proxy, scanning_proxy


class Wemo(scanning_proxy.ScanningProxy):
  """Hue proxy object."""

  def __init__(self, refresh_period, callback):
    super(Wemo, self).__init__(refresh_period)

    self._callback = callback
    self._devices = {}
    self._state_cache = {}
    self._subscriptions = pywemo.SubscriptionRegistry()
    self._subscriptions.start()


  def _scan_once(self):
    devices = pywemo.discover_devices()

    logging.info('Found %d wemo devices.', len(devices))

    for device in devices:
      device_exists = device.serialnumber in self._devices
      self._devices[device.serialnumber] = device

      state = device.get_state()
      serialnumber = device.serialnumber
      state_changed = state != self._state_cache.get(serialnumber, None)
      self._state_cache[serialnumber] = state

      details = {
          'serial_number': serialnumber,
          'model': device.model,
          'name': device.name,
          'state': state == 1
      }

      if not device_exists:
        self._subscriptions.register(device)
        self._subscriptions.on(device, 'BinaryState', self._event)

      device_type = self.get_type(device)
      if device_type is None:
        return

      if not device_exists or state_changed:
        self._callback(device_type, 'wemo-%s' % device.serialnumber, details)

  def get_type(self, device):
    uuid = device._config.UDN
    if uuid.startswith('uuid:Socket'):
      return 'wemo_switch'
    #elif uuid.startswith('uuid:Lightswitch'):
    #    return LightSwitch(location)
    #elif uuid.startswith('uuid:Insight'):
    #    return Insight(location)
    elif uuid.startswith('uuid:Sensor'):
      return 'wemo_motion'
    else:
      return None

  @proxy.command
  def set_state(self, serial_number, state):
    device = self._devices.get(serial_number)
    if not device:
      logging.error('Device "%s" not found', serial_number)
      return

    device.set_state(1 if state else 0)

  def _event(self, device, value):
    device_type = self.get_type(device)
    if device_type is None:
      return

    details = {
      'serial_number': device.serialnumber,
      'model': device.model,
      'name': device.name,
      'state': int(value) == 1
    }

    self._callback(device_type, 'wemo-%s' % device.serialnumber, details)

  def stop(self):
    super(Wemo, self).stop()
    self._subscriptions.stop()

  def join(self):
    super(Wemo, self).join()
    self._subscriptions.join()
