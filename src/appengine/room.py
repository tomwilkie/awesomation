"""ROOMs"""
import logging

from google.appengine.ext import db
from google.appengine.ext import ndb

import flask

from appengine import device, user, model


def command(func):
  """Device command decorator - automatically dispatches methods."""
  setattr(func, 'is_command', True)
  return func


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

  @command
  def all_on(self):
    switches = device.Switch.query().filter(
        device.Device.room == self.key).iter()
    for switch in switches:
      switch.turn_on()

  @command
  def all_off(self):
    switches = device.Switch.query().filter(
        device.Device.room == self.key).iter()
    for switch in switches:
      switch.turn_off()


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)


@blueprint.route('/', methods=['GET'])
def get_rooms():
  """Return json list of devices."""
  room_list = Room.query().iter()
  if room_list is None:
    room_list = []

  room_list = [room.to_dict() for room in room_list]
  return flask.jsonify(rooms=room_list)


@blueprint.route('/<room_id>', methods=['POST'])
def create_update_room(room_id):
  """Using json body to create or update a room."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  room = Room.get_by_id(room_id)

  if not room:
    room = Room(id=room_id, owner=user_id)

  elif room.owner != user_id:
    flask.abort(403)

  # Update the object; abort with 400 on unknown field
  try:
    room.populate(**body)
  except AttributeError, err:
    flask.abort(400)

  # Put the object - BadValueError if there are uninitalised required fields
  try:
    room.put()
  except db.BadValueError, err:
    flask.abort(400)

  return flask.jsonify(**room.to_dict())

@blueprint.route('/<room_id>/command', methods=['POST'])
def room_command(room_id):
  """Using json body to create or update a device."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  room = Room.get_by_id(room_id)

  if not room:
    flask.abort(404)
  elif room.owner != user_id:
    flask.abort(403)

  room.handle_command(body)

  return ('', 204)
