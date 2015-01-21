"""Drivers for TKB zwave devices."""

from appengine.devices import zwave


@zwave.register(manufacturer_id='0118', product_type='0202', product_id='0611')
class TKBMultilevelPowerSwitch(zwave.Driver):
  """Driver for TKB Multilevel power switch."""

  def get_capabilities(self):
    return ['SWITCH', 'DIMMABLE']

  def get_categories(self):
    return ['LIGHTING']

  def value_changed(self, event):
    """We've been told a value changed; deal with it."""
    value = event['valueId']
    if value['commandClass'] == 'COMMAND_CLASS_SWITCH_MULTILEVEL':
      self._device.brightness = value['value']

  def sync(self):
    ccv = self._device.get_command_class_value(
        'COMMAND_CLASS_SWITCH_MULTILEVEL', 0)
    ccv.set_value(self._device.brightness if self._device.state else 0)
