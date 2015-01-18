"""Generic device driver for 433mhz switches."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('rfswitch')
class RFSwitch(device.Switch):
  """A 433mhz rf switch."""
  system_code = ndb.StringProperty(required=True)
  device_code = ndb.IntegerProperty(required=True)

  def sync(self):
    event = {'type': 'rfswitch', 'command': 'set_state',
             'system_code': self.system_code,
             'device_code': self.device_code, 'mode': self.state}
    pushrpc.send_event(event)
