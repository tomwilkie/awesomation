"""Philips hue integration."""

import logging

from google.appengine.ext import ndb

from appengine import model, pushrpc


class HueBridge(model.Device):
  """A hue bridge."""
  linked = ndb.BooleanProperty(required=True)

  def handle_command(self, command):
    if command['command'] == 'scan':
      event = {'type': 'hue', 'command': 'scan'}
      pushrpc.send_event(self.owner, event)
    else:
      logging.error('Unknown command %s', command['type'])

  def handle_event(self, event):
    """Handle a device update event."""
    # Only events are when we find a bridge,
    # and we are told the name and linked status

    self.name = event['name']
    self.linked = event['linked']


class HueLight(model.Device):
  pass
