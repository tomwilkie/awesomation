"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('wemo')
class WemoDevice(device.Switch):
  """A hue light."""
  serial_number = ndb.StringProperty(required=True)
  model = ndb.StringProperty()
  state = ndb.IntegerProperty()

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'wemo', 'command': 'scan'}
    pushrpc.send_event(event)

  def sync(self):
    """Update the state of a light."""
    event = {'type': 'wemo',
             'command': 'set_state',
             'serial_number': self.serial_number,
             'state': 1 if self.state else 0}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    self.device_name = event['name']
    self.serial_number = event['serial_number']
    self.model = event['model']
    self.state = event['state']
