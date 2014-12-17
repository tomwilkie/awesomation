"""rf433 device proxy code."""

import logging

import rcswitch

from pi import proxy


class RFSwitch(proxy.Proxy):
  """433mhz RF Switch proxy implementation."""

  def __init__(self, pin, repeats=5):
    self._switch = rcswitch.RCSwitch()
    self._switch.enableTransmit(pin)
    self._repeats = repeats

  @proxy.command
  def set_state(self, system_code, device_code, mode):
    """Handle rf swtich events - turn it on or off."""
    system_code = str(system_code)
    device_code = int(device_code)
    logging.info('system_code = %s, device_code = %s, mode = %s',
                 system_code, device_code, mode)

    for _ in xrange(self._repeats):
      if mode:
        self._switch.switchOn(system_code, device_code)
      else:
        self._switch.switchOff(system_code, device_code)

  def stop(self):
    pass
