"""Philips hue integration."""

import logging
import re

from google.appengine.ext import ndb

from appengine import device, pushrpc, rest


@device.register('hue_bridge')
class HueBridge(device.Device):
  """A hue bridge."""
  linked = ndb.BooleanProperty(required=True)

  def get_capabilities(self):
    return ['SCAN']

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'hue', 'command': 'scan'}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    # Only events are when we find a bridge,
    # and we are told the name and linked status

    self.name = event['name']
    self.linked = event['linked']


LIGHT_ID_RE = re.compile(r'hue-([0-9a-f]+)-([0-9]+)')


@device.register('hue_light')
class HueLight(device.Switch):
  """A hue light."""
  hue_type = ndb.StringProperty()
  hue_model_id = ndb.StringProperty()

  @rest.command
  def turn_on(self):
    self.state = True
    self._set_state(True)

  @rest.command
  def turn_off(self):
    self.state = False
    self._set_state(False)

  def _set_state(self, state):
    """Update the state of a light."""
    match = LIGHT_ID_RE.match(self.key.id())
    bridge_id = match.group(1)
    device_id = int(match.group(2))

    event = {'type': 'hue',
             'command': 'set_state',
             'bridge_id': bridge_id,
             'device_id': device_id,
             'mode': state}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    logging.info(event)
    self.name = event['name']
    self.hue_type = event['type']
    self.hue_model_id = event['modelid']

    state = event['state']
    self.state = state['on']
