"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


class WemoMixin(object):
  """All wemo's have a model and serial number in common."""
  serial_number = ndb.StringProperty(required=True)
  model = ndb.StringProperty()

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'wemo', 'command': 'scan'}
    pushrpc.send_event(event)

  def handle_event(self, event):
    self.device_name = event['name']
    self.serial_number = event['serial_number']
    self.model = event['model']


@device.register('wemo_motion')
class WemoMotion(device.Device, WemoMixin, device.DetectorMixin):
  """A Wemo Motion Sensor"""

  def get_capabilities(self):
    return ['OCCUPIED']

  def get_categories(self):
    return ['CLIMATE']

  def handle_event(self, event):
    """Handle a device update event."""
    WemoMixin.handle_event(self, event)
    self.real_occupied_state_change(event['state'])


@device.register('wemo_switch')
class WemoSwitch(device.Switch, WemoMixin):
  """A Wemo switch."""
  def sync(self):
    """Update the state of a light."""
    event = {'type': 'wemo',
             'command': 'set_state',
             'serial_number': self.serial_number,
             'state': self.state}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    WemoMixin.handle_event(self, event)
    self.state = event['state']
