"""Factory for creating devices."""
import logging

from google.appengine.api import namespace_manager
from google.appengine.ext import db
from google.appengine.ext import ndb

import flask

from appengine import model, user
from appengine import room as room_module


DEVICE_TYPES = {}


def command(func):
  """Device command decorator - automatically dispatches methods."""
  func.is_command = True
  return func


def register(device_type):
  """Decorator to cause device types to be registered."""
  def class_rebuilder(cls):
    DEVICE_TYPES[device_type] = cls
    return cls
  return class_rebuilder


def create_device(device_id, device_type, user_id):
  """Factory for creating new devices."""
  constructor = DEVICE_TYPES.get(device_type, None)
  if constructor is None:
    flask.abort(400)
  return constructor(id=device_id, owner=user_id)


class Device(model.Base):
  """Base class for all device drivers."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  last_update = ndb.DateTimeProperty(required=False, auto_now=True)
  room = ndb.KeyProperty()

  def handle_event(self, event):
    pass

  def handle_command(self, command_dict):
    """Dispatch command to appropriate handler."""
    logging.info(command_dict)
    func_name = command_dict.pop('command', None)
    func = getattr(self, func_name, None)
    if func is None or not func.is_command:
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)
    func(**command_dict)

  @command
  def set_room(self, room_id):
    """Change the room associated with this device."""
    room = room_module.Room.get_by_id(room_id)
    if not room:
      flask.abort(404)
    room.devices.append(self.key)
    room.put()

    self.room = room.key
    self.put()


class Switch(Device):
  """A swtich."""
  state = ndb.BooleanProperty()

  @command
  def turn_on(self):
    pass

  @command
  def turn_off(self):
    pass


# pylint: disable=invalid-name
blueprint = flask.Blueprint('device', __name__)


@blueprint.route('/events', methods=['POST'])
def handle_events():
  """Handle events from devices."""
  user_id = '102063417381751091397'
  namespace_manager.set_namespace(user_id)

  events = flask.request.get_json()
  logging.info('Processing %d events', len(events))

  device_cache = {}

  for event in events:
    device_type = event['device_type']
    device_id = event['device_id']
    event_body = event['event']

    if device_id in device_cache:
      device = device_cache[device_id]
    else:
      device = Device.get_by_id(device_id)
      if not device:
        device = create_device(device_id, device_type, user_id)
      device_cache[device_id] = device

    device.handle_event(event_body)

  for device in device_cache.itervalues():
    device.put()

  return ('', 204)


@blueprint.route('/', methods=['GET'])
def list_devices():
  """Return json list of devices."""
  device_list = Device.query().iter()
  if device_list is None:
    device_list = []

  device_list = [device.to_dict() for device in device_list]
  return flask.jsonify(devices=device_list)


@blueprint.route('/<device_id>', methods=['POST'])
def create_update_device(device_id):
  """Using json body to create or update a device."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  device = Device.get_by_id(device_id)

  if not device:
    device_type = body.pop('type', None)
    if device_type is None:
      flask.abort(400, '\'type\' field expected in body.')

    device = create_device(
        device_id, device_type, user_id)

  elif device.owner != user_id:
    flask.abort(403)

  # Update the object; abort with 400 on unknown field
  try:
    device.populate(**body)
  except AttributeError, err:
    flask.abort(400)

  # Put the object - BadValueError if there are uninitalised required fields
  try:
    device.put()
  except db.BadValueError, err:
    flask.abort(400)

  return flask.jsonify(**device.to_dict())


@blueprint.route('/<device_id>', methods=['GET'])
def get_device(device_id):
  """Return json repr of given device."""
  user_id = user.get_user()
  device = Device.get_by_id(device_id)

  if not device:
    flask.abort(404)
  elif device.owner != user_id:
    flask.abort(403)

  return flask.jsonify(**device.to_dict())


@blueprint.route('/<device_id>/command', methods=['POST'])
def device_command(device_id):
  """Using json body to create or update a device."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  device = Device.get_by_id(device_id)

  if not device:
    flask.abort(404)
  elif device.owner != user_id:
    flask.abort(403)

  device.handle_command(body)

  return ('', 204)

