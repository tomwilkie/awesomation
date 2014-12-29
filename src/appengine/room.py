"""ROOMs"""
import logging

from google.appengine.ext import ndb

import flask

from appengine import device, model, rest


class Room(model.Base):
  """A room in a property."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  devices = ndb.KeyProperty(repeated=True)

  def handle_command(self, command_dict):
    """Dispatch command to appropriate handler."""
    logging.info(command_dict)
    func_name = command_dict.pop('command', None)
    func = getattr(self, func_name, None)
    logging.info('%s %s %s', func, type(func), func.is_command)
    if func is None or not func.is_command:
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)
    func(**command_dict)

  @rest.command
  def all_on(self):
    switches = device.Switch.query().filter(
        device.Device.room == self.key).iter()
    for switch in switches:
      switch.turn_on()

  @rest.command
  def all_off(self):
    switches = device.Switch.query().filter(
        device.Device.room == self.key).iter()
    for switch in switches:
      switch.turn_off()


def create_room(room_id, user_id, _body):
  return Room(id=room_id, owner=user_id)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)
rest.register_class(blueprint, Room, create_room)
