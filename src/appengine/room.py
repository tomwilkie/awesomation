"""ROOMs"""

from google.appengine.ext import db
from google.appengine.ext import ndb

import flask

from appengine import user, model


class Room(model.Base):
  """A room in a property."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  devices = ndb.KeyProperty(repeated=True)


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
