"""Factory for creating devices."""

from appengine import door, ios, zwave

def create_device(device_id, device_type, params=None):
  if params is None:
    params = {}

  if device_type == 'ios':
    return ios.IosDevice(key_name=device_id, **params)
  elif device_type == 'door':
    return door.Door(key_name=device_id, **params)
  elif device_type == 'zwave':
    return zwave.ZWaveDevice(key_name=device_id)
  else:
    assert False
