"""Philips hue integration."""

from appengine import device, model, pushrpc


@device.register('sonos')
class SonosDevice(device.Device):
  """A hue light."""
  uid = model.Property()
  state = model.Property()
  currently_playing = model.Property()

  def get_categories(self):
    return ['MUSIC']

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'sonos', 'command': 'scan'}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    self.populate(**event)

