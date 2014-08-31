import ios

def CreateDevice(device_id, params):
  if params['type'] == 'ios':
    return ios.IosDevice(key_name=device_id, **params)
  elif params['type'] == 'door':
    return door.Door(key_name=device_id, **params)
  else:
    assert False