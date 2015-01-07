"""ROOMs"""

from google.appengine.ext import ndb

import flask

from appengine import device, model, rest


class Room(model.Base):
  """A room in a property."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)

  @rest.command
  def all_on(self):
    switches = (device.Device.get_by_capability('SWITCH')
                .filter(device.Device.room == self.key).iter())
    for switch in switches:
      switch.turn_on()

  @rest.command
  def all_off(self):
    switches = (device.Device.get_by_capability('SWITCH')
                .filter(device.Device.room == self.key).iter())
    for switch in switches:
      switch.turn_off()


def create_room(room_id, user_id, _):
  return Room(id=room_id, owner=user_id)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)
rest.register_class(blueprint, Room, create_room)
