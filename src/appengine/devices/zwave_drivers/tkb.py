"""Drivers for TKB zwave devices."""

from appengine import rest
from appengine.devices import zwave


@zwave.register(manufacturer_id='0118', product_type='0202', product_id='0611')
class TKBMultilevelPowerSwitch(zwave.Driver):
  """Driver for TKB Multilevel power switch."""

  def get_capabilities(self):
    return ['SWITCH']

  @rest.command
  def turn_on(self):
    self._device.state = True
    ccv = self._device.get_command_class_value('COMMAND_CLASS_SWITCH_MULTILEVEL', 0)
    ccv.set_value(255)

  @rest.command
  def turn_off(self):
    self._device.state = False
    ccv = self._device.get_command_class_value('COMMAND_CLASS_SWITCH_MULTILEVEL', 0)
    ccv.set_value(0)
