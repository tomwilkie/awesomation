"""Drivers for Aeon Labs zwave devices."""

from appengine.devices import zwave

@zwave.register(manufacturer_id='0086', product_type='0002', product_id='0005')
class AeonLabsMultiSensor(zwave.Driver):
  """Driver for Aeon Labs Multi Sensor."""

  def _set(self, command_class, index, intended_value):
    ccv = self._device.get_command_class_value(command_class, index)
    if ccv.value != intended_value:
      ccv.set_value(intended_value)

  def configure_device(self):
    """Configure this device to send value changes (instead of basic set),
       on motion, and temp, humidity and luminance every 5 mins."""
    self._set('COMMAND_CLASS_CONFIGURATION', 4, 'Binary Sensor Report')
    self._set('COMMAND_CLASS_CONFIGURATION', 101, 0b11100001)
    self._set('COMMAND_CLASS_CONFIGURATION', 111, 5*60)

  def handle_event(self, event):
    if event['notificationType'] in {zwave.NODE_ADDED, zwave.NODE_INFO_UPDATE}:
      self.configure_device()

