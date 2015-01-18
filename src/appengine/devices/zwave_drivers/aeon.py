"""Drivers for Aeon Labs zwave devices."""

from appengine.devices import zwave

@zwave.register(manufacturer_id='0086', product_type='0002', product_id='0005')
class AeonLabsMultiSensor(zwave.Driver):
  """Driver for Aeon Labs Multi Sensor."""
  CONFIGURATION = {
    ('COMMAND_CLASS_CONFIGURATION', 4): 'Binary Sensor Report',
    ('COMMAND_CLASS_CONFIGURATION', 101): 0b11100001,
    ('COMMAND_CLASS_CONFIGURATION', 111): 5*60
  }

  def handle_event(self, event):
    if event['notificationType'] in {zwave.NODE_ADDED, zwave.NODE_INFO_UPDATE}:
      if not self.is_configured():
        self.configure()

