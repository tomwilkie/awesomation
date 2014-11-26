"""Generic Z Wave device driver."""

import logging

from google.appengine.ext import db

from appengine import model


class ZWaveDevice(model.Device):
  """Generic Z Wave device driver."""
  zwave_device_id = db.IntegerProperty(required=False)
  zwave_home_id = db.IntegerProperty(required=False)

  def handle_event(self, event):
    """Handle an event form the zwave device."""
    notification_type = event['notificationType']
    home_id = event['homeId']
    node_id = event['nodeId']

    if notification_type in {'ValueAdded', 'ValueChanged'}:
      value = event['valueId']
      command_class = value.pop('commandClass')
      index = value.pop('index')
      del value['homeId']
      del value['nodeId']

      logging.info(self, home_id, node_id, command_class, index, value)

      #self._devices[node_id]['command_classes'][command_class][index] = value
      #logging.info(self._devices)
      #self._devices[node_id] = {'command_classes':
      # collections.defaultdict(dict)}
