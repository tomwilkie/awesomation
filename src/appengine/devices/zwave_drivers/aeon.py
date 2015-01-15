"""Drivers for Aeon Labs zwave devices."""

from appengine.devices import zwave

@zwave.register(manufacturer_id='0086', product_type='0002', product_id='0005')
class AeonLabsMultiSensor(zwave.Driver):
  pass
