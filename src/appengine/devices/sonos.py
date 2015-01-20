"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('sonos')
class SonosDevice(device.Device):
  """A hue light."""
  uid = ndb.StringProperty(required=True)
  state = ndb.StringProperty()
  currently_playing = ndb.JsonProperty()

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

