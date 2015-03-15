"""Drivers for Fibaro zwave devices."""
from appengine.devices import zwave


@zwave.register(manufacturer_id='010f', product_type='0800', product_id='1001')
class FibaroMotionSensor(zwave.Driver):
  """Driver for Fibaro Motion Sensor."""
  CONFIGURATION = {
      # Send illumination reports every 5 mins
      ('COMMAND_CLASS_CONFIGURATION', 42): 5*60,

      # Send temperature reports every 5 mins
      ('COMMAND_CLASS_CONFIGURATION', 64): 5*60,
  }

  def get_capabilities(self):
    return super(FibaroMotionSensor, self).get_capabilities() + ['OCCUPIED']

  def get_categories(self):
    return ['CLIMATE']

  def value_changed(self, event):
    """We've been told a value changed; deal with it."""
    value = event['valueId']
    if value['commandClass'] == 'COMMAND_CLASS_SENSOR_MULTILEVEL':
      if value['index'] == 1:
        self._device.temperature = value['value']
      elif value['index'] == 3:
        self._device.lux = value['value']

    if value['commandClass'] == 'COMMAND_CLASS_SENSOR_BINARY':
      self._device.real_occupied_state_change(value['value'])

