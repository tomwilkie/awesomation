"""Philips hue integration."""

import logging
import re

from google.appengine.ext import ndb

from appengine import device, pushrpc


@device.register('hue_bridge')
class HueBridge(device.Device):
  """A hue bridge."""
  linked = ndb.BooleanProperty(required=True)

  def get_capabilities(self):
    return ['SCAN']

  def get_categories(self):
    return ['LIGHTING']

  @classmethod
  @device.static_command
  def scan(cls):
    event = {'type': 'hue', 'command': 'scan'}
    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    # Only events are when we find a bridge,
    # and we are told the name and linked status

    self.device_name = event['name']
    self.linked = event['linked']


LIGHT_ID_RE = re.compile(r'hue-([0-9a-f]+)-([0-9]+)')


@device.register('hue_light')
class HueLight(device.Switch):
  """A hue light."""
  hue_type = ndb.StringProperty()
  hue_model_id = ndb.StringProperty()
  brightness = ndb.IntegerProperty() # 0 - 255
  color_temperature = ndb.IntegerProperty() # 153 - 500

  def get_capabilities(self):
    capabilities = ['SWITCH', 'DIMMABLE']
    if self.hue_model_id == 'LCT001':
      capabilities.append('COLOR_TEMPERATURE')
    return capabilities

  def sync(self):
    """Update the state of a light."""
    match = LIGHT_ID_RE.match(self.key.id())
    bridge_id = match.group(1)
    device_id = int(match.group(2))

    event = {'type': 'hue',
             'command': 'set_state',
             'bridge_id': bridge_id,
             'device_id': device_id,
             'mode': self.state,
             'brightness': self.brightness,
             'color_temperature': self.color_temperature}

    pushrpc.send_event(event)

  def handle_event(self, event):
    """Handle a device update event."""
    logging.info(event)

    self.device_name = event['name']
    self.hue_type = event['type']
    self.hue_model_id = event['modelid']

    state = event['state']
    self.state = state['on']
    self.brightness = state['bri']
    self.color_temperature = state.get('ct', None)
