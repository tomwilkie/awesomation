"""Philips hue integration."""

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('sonos')
class SonosDevice(device.Device):
  """A hue light."""
  uid = ndb.StringProperty(required=True)

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'sonos', 'command': 'scan'}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    self.device_name = event['name']
    self.uid = event['uid']

