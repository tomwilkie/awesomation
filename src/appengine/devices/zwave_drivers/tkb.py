"""Drivers for TKB zwave devices."""

from appengine.devices import zwave


@zwave.register(manufacturer_id='0118', product_type='0202', product_id='0611')
class TKBMultilevelPowerSwitch(zwave.Driver):
  """Driver for TKB Multilevel power switch."""
  # Device seems to only support 0-100, so scale our 0-255 range

  def get_capabilities(self):
    return super(TKBMultilevelPowerSwitch, self).get_capabilities() \
       + ['SWITCH', 'DIMMABLE']

  def get_categories(self):
    return ['LIGHTING']

  def value_changed(self, event):
    """We've been told a value changed; deal with it."""
    value = event['valueId']
    if value['commandClass'] == 'COMMAND_CLASS_SWITCH_MULTILEVEL':
      # We treat brightness and state separately, but this
      # device does not.  Attempt to fake it by ignoring
      # brightness going to zero.
      if self._device.state and value['value'] > 0:
        self._device.brightness = value['value'] * 255 / 100
      else:
        self._device.state = False

  def sync(self):
    ccv = self._device.get_command_class_value(
        'COMMAND_CLASS_SWITCH_MULTILEVEL', 0)

    if self._device.brightness is None:
      self._device.brightness = 0

    if self._device.state:
      value = self._device.brightness * 100 / 255
    else:
      value = 0
    ccv.set_value(value)
