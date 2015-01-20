"""Drivers for Aeon Labs zwave devices."""
from appengine import room
from appengine.devices import zwave


@zwave.register(manufacturer_id='0086', product_type='0002', product_id='0005')
class AeonLabsMultiSensor(zwave.Driver):
  """Driver for Aeon Labs Multi Sensor."""
  CONFIGURATION = {
      ('COMMAND_CLASS_CONFIGURATION', 5): 'Binary Sensor Report',
      ('COMMAND_CLASS_CONFIGURATION', 101): 0b11100001,
      ('COMMAND_CLASS_CONFIGURATION', 111): 5*60
  }

  def get_capabilities(self):
    return ['OCCUPIED']

  def get_categories(self):
    return ['CLIMATE']

  def value_changed(self, event):
    """We've been told a value changed; deal with it."""
    value = event['valueId']
    if value['commandClass'] != 'COMMAND_CLASS_SENSOR_BINARY':
      return

    self._device.occupied = value['value']

    # Now tell the room to update its lights
    if not self._device.room:
      return

    room_obj = room.Room.get_by_id(self._device.room)
    if not room_obj:
      return

    room_obj.update_lights()

  def handle_event(self, event):
    if event['notificationType'] in {zwave.NODE_ADDED, zwave.NODE_INFO_UPDATE}:
      if not self.is_configured():
        self.configure()

    elif event['notificationType'] in {zwave.NODE_VALUE_CHANGED,
                                       zwave.NODE_VALUE_ADDED}:
      self.value_changed(event)

