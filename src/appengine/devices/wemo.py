"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc, rest


@device.register('wemo')
class WemoDevice(device.Switch):
  """A hue light."""
  serial_number = ndb.StringProperty(required=True)
  model = ndb.StringProperty()
  state = ndb.IntegerProperty()

  def __init__(self, **kwargs):
    super(WemoDevice, self).__init__(**kwargs)
    self.capabilities = ['SWITCH']

  @rest.command
  def turn_on(self):
    self.state = 1
    self._set_state(1)

  @rest.command
  def turn_off(self):
    self.state = 0
    self._set_state(0)

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'wemo', 'command': 'scan'}
    pushrpc.send_event(event)

  def _set_state(self, state):
    """Update the state of a light."""
    event = {'type': 'wemo',
             'command': 'set_state',
             'serial_number': self.serial_number,
             'state': 1 if state else 0}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    self.name = event['name']
    self.serial_number = event['serial_number']
    self.model = event['model']
    self.state = event['state']
