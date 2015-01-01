"""Factory for creating devices."""
import logging

from google.appengine.api import namespace_manager
from google.appengine.ext import ndb

import flask

from appengine import model, pushrpc, rest


DEVICE_TYPES = {}


def static_command(func):
  """Device command decorator - automatically dispatches methods."""
  setattr(func, 'is_command', True)
  setattr(func, 'is_static', True)
  return func


def register(device_type):
  """Decorator to cause device types to be registered."""
  def class_rebuilder(cls):
    DEVICE_TYPES[device_type] = cls
    return cls
  return class_rebuilder


def create_device(device_id, user_id, body):
  """Factory for creating new devices."""
  device_type = body.pop('type', None)
  if device_type is None:
    flask.abort(400, '\'type\' field expected in body.')

  constructor = DEVICE_TYPES.get(device_type, None)
  if constructor is None:
    logging.error('No device type \'%s\'', device_type)
    flask.abort(400)
  return constructor(id=device_id, owner=user_id)


class Device(model.Base):
  """Base class for all device drivers."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  last_update = ndb.DateTimeProperty(required=False, auto_now=True)
  room = ndb.KeyProperty('room')
  capabilities = ndb.ComputedProperty(lambda self: self.get_capabilities(),
                                      repeated=True)

  def get_capabilities(self):
    return []

  def handle_event(self, event):
    pass

  @classmethod
  def get_by_capability(cls, capability):
    return cls.query(Device.capabilities == capability)

  @classmethod
  def handle_static_command(cls, command_dict):
    """Dispatch command to appropriate handler."""
    logging.info(command_dict)
    func_name = command_dict.pop('command', None)
    func = getattr(cls, func_name, None)
    logging.info('%s %s %s', func, type(func), func.is_command)
    if func is None or not func.is_command or not func.is_static:
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)
    func(**command_dict)

  @rest.command
  def set_room(self, room_id):
    """Change the room associated with this device."""
    from appengine import room as room_module
    room = room_module.Room.get_by_id(room_id)
    if not room:
      flask.abort(404)
    room.devices.append(self.key)
    room.put()

    self.room = room.key
    self.put()

  def list_commands(self):
    """List commands on this device."""
    methods = (getattr(self, method)
               for method in dir(self))
    methods = (method for method in methods
               if callable(method)
               and method.is_command)
    methods = [{'name': method.__name__}
               for method in methods]
    return methods


class Switch(Device):
  """A swtich."""
  state = ndb.BooleanProperty()

  def get_capabilities(self):
    return ['SWITCH']

  @rest.command
  def turn_on(self):
    pass

  @rest.command
  def turn_off(self):
    pass


# pylint: disable=invalid-name
blueprint = flask.Blueprint('device', __name__)
rest.register_class(blueprint, Device, create_device)


@blueprint.route('/events', methods=['POST'])
def handle_events():
  """Handle events from devices."""
  proxy = pushrpc.authenticate()
  if proxy is None:
    flask.abort(401)

  # If proxy hasn't been claimed, not much we can do.
  if proxy.owner is None:
    logging.info('Dropping events as this proxy is not claimed')
    return ('', 204)

  # We need to set namespace - not done by main.py
  namespace_manager.set_namespace(proxy.owner)

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
        device = create_device(device_id, device_type, proxy.owner)
      device_cache[device_id] = device

    device.handle_event(event_body)

  for device in device_cache.itervalues():
    device.put()

  return ('', 204)


