"""Generic device driver for 433mhz switches."""

from appengine import device, model, pushrpc


@device.register('rfswitch')
class RFSwitch(device.Switch):
  """A 433mhz rf switch."""
  system_code = model.Property()
  device_code = model.Property()

  def sync(self):
    event = {'type': 'rfswitch', 'command': 'set_state',
             'system_code': self.system_code,
             'device_code': self.device_code, 'mode': self.state}
    pushrpc.send_event(event)
