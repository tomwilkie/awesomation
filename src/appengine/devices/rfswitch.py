"""Generic device driver for 433mhz switches."""

from google.appengine.ext import ndb

from appengine import device, pushrpc, rest


@device.register('rfswitch')
class RFSwitch(device.Switch):
  """A 433mhz rf switch."""
  system_code = ndb.StringProperty(required=True)
  device_code = ndb.IntegerProperty(required=True)

  def _set_value(self, value):
    event = {'type': 'rfswitch', 'command': 'set_state',
             'system_code': self.system_code,
             'device_code': self.device_code, 'mode': value}
    pushrpc.send_event(event)

  @rest.command
  def turn_on(self):
    self.state = True
    self._set_value(True)

  @rest.command
  def turn_off(self):
    self.state = False
    self._set_value(False)
