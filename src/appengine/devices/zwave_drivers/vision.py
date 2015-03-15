"""Drivers for Vision zwave devices."""
from appengine.devices import zwave


@zwave.register(manufacturer_id='0109', product_type='2002', product_id='0203')
class VisionMotionSensor(zwave.Driver):
  """Driver for Vision Motion Sensor."""
  #CONFIGURATION = {
  #    ('COMMAND_CLASS_CONFIGURATION', 5): 'Binary Sensor Report',
  #    ('COMMAND_CLASS_CONFIGURATION', 101): 0b11100001,
  #    ('COMMAND_CLASS_CONFIGURATION', 111): 5*60
  #}

  def get_capabilities(self):
    return super(VisionMotionSensor, self).get_capabilities() + ['OCCUPIED']

  def get_categories(self):
    return ['CLIMATE']

  def value_changed(self, event):
    """We've been told a value changed; deal with it."""
    value = event['valueId']
    if value['commandClass'] == 'COMMAND_CLASS_SENSOR_MULTILEVEL':
      if value['index'] == 1:
        self._device.temperature = value['value']

    if value['commandClass'] == 'COMMAND_CLASS_SENSOR_BINARY':
      self._device.real_occupied_state_change(value['value'])

