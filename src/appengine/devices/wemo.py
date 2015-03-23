"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


class WemoBase(device.Device):
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
class WemoMotion(WemoBase, device.DetectorMixin):
  """A Wemo Motion Sensor"""

  def get_capabilities(self):
    return ['OCCUPIED']

  def get_categories(self):
    return ['CLIMATE']

  def handle_event(self, event):
    """Handle a device update event."""
    super(WemoMotion, self).handle_event(event)
    self.real_occupied_state_change(event['state'])


@device.register('wemo_switch')
class WemoSwitch(WemoBase):
  """A Wemo switch."""
  state = ndb.IntegerProperty()

  def get_capabilities(self):
    return ['SWITCH']

  def get_categories(self):
    return ['LIGHTING']

  def sync(self):
    """Update the state of a light."""
    event = {'type': 'wemo',
             'command': 'set_state',
             'serial_number': self.serial_number,
             'state': 1 if self.state else 0}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    super(WemoSwitch, self).handle_event(event)
    self.state = event['state']
