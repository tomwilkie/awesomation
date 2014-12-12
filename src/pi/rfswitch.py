"""rf433 device proxy code."""

import logging

import rcswitch


class RFSwitch(object):
  """433mhz RF Switch proxy implementation."""

  def __init__(self, pin, repeats=5):
    self._switch = rcswitch.RCSwitch()
    self._switch.enableTransmit(pin)
    self._repeats = repeats

  def handle_events(self, messages):
    """Handle rf swtich events - turn it on or off."""
    for _ in xrange(self._repeats):
      for message in messages:
        system_code = str(message["system_code"])
        device_code = int(message["device_code"])
        mode = message["mode"]

        logging.info('system_code = %s, device_code = %s, mode = %s',
                     system_code, device_code, mode)
        if mode:
          self._switch.switchOn(system_code, device_code)
        else:
          self._switch.switchOff(system_code, device_code)

  def stop(self):
    pass
