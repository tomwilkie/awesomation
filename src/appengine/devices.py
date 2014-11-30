"""Factory for creating devices."""

from appengine import door, hue, ios, rfswitch, zwave


def create_device(device_id, device_type, user_id):

  if device_type == 'ios':
    return ios.IosDevice(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'door':
    return door.Door(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'zwave':
    return zwave.ZWaveDevice(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'rfswitch':
    return rfswitch.RFSwitch(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'hue_bridge':
    return hue.HueBridge(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'hue_light':
    return hue.HueLight(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  else:
    assert False
