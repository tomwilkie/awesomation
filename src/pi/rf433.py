import rcswitch


class RF433(object):
  
  def __init__(self, pin):
    self._switch = rcswitch.RCSwitch()
    self._switch.enableTransmit(pin)

  def HandleMessage(self, message):
    system_code = message["system_code"]
    device_code = int(message["device_code"])
  
    if message["mode"]:
      self._switch.switchOn(system_code, device_code)
    else:
      self._switch.switchOff(system_code, device_code)
