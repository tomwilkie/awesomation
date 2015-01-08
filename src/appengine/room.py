"""ROOMs"""
from google.appengine.ext import ndb

import flask

from appengine import device, model, rest


class Room(model.Base):
  """A room in a property."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)

  @classmethod
  def _event_classname(cls):
    return 'room'

  def set_lights(self, value):
    """Set all the lights in this room on/off."""
    switches = (device.Device.get_by_capability('SWITCH')
                .filter(device.Device.room == self.key.string_id()).iter())
    # We want to iterate over this twice.
    switches = list(switches)

    for switch in switches:
      if value:
        switch.turn_on()
      else:
        switch.turn_off()
    ndb.put_multi(switches)

  @rest.command
  def all_on(self):
    self.set_lights(True)

  @rest.command
  def all_off(self):
    self.set_lights(False)


def create_room(room_id, user_id, _):
  return Room(id=room_id, owner=user_id)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)
rest.register_class(blueprint, Room, create_room)
