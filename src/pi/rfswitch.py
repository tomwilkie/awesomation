"""rf433 device proxy code."""

import logging

import rcswitch


class RFSwitch(object):
  """433mhz RF Switch proxy implementation."""

  def __init__(self, pin):
    self._switch = rcswitch.RCSwitch()
    self._switch.enableTransmit(pin)

  def handle_event(self, message):
    """Handle rf swtich events - turn it on or off."""
    system_code = str(message["system_code"])
    device_code = int(message["device_code"])
    mode = message["mode"]

    logging.info('system_code = %s (%s), device_code = %s (%s), mode = %s',
                 system_code, type(system_code), device_code,
                 type(device_code), mode)

    if mode:
      self._switch.switchOn(system_code, device_code)
    else:
      self._switch.switchOff(system_code, device_code)

  def stop(self):
    pass
