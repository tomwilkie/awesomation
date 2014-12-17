"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('wemo')
class WemoDevice(device.Switch):
  """A hue light."""
  serial_number = ndb.StringProperty(required=True)
  model = ndb.StringProperty()
  state = ndb.IntegerProperty()

  @device.command
  def turn_on(self):
    self.state = 1
    self._set_state(1)

  @device.command
  def turn_off(self):
    self.state = 0
    self._set_state(0)

  @classmethod
  @device.static_command
  def scan(cls, user_id):
    event = {'type': 'wemo', 'command': 'scan'}
    pushrpc.send_event(user_id, event)

  def _set_state(self, state):
    """Update the state of a light."""
    event = {'type': 'wemo',
             'command': 'set_state',
             'serial_number': self.serial_number,
             'state': 1 if state else 0}
    pushrpc.send_event(self.owner, event)

  def handle_event(self, event):
    """Handle a device update event."""
    self.name = event['name']
    self.serial_number = event['serial_number']
    self.model = event['model']
    self.state = event['state']
