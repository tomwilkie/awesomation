"""Factory for creating devices."""
import logging

from google.appengine.api import namespace_manager
from google.appengine.ext import ndb

import flask

from appengine import model, pushrpc, rest
from common import detector


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


def create_device(device_id, body, device_type=None):
  """Factory for creating new devices."""
  if device_type is None:
    device_type = body.pop('type', None)

  if device_type is None:
    flask.abort(400, '\'type\' field expected in body.')

  constructor = DEVICE_TYPES.get(device_type, None)
  if constructor is None:
    logging.error('No device type \'%s\'', device_type)
    flask.abort(400)
  return constructor(id=device_id)


class Device(model.Base):
  """Base class for all device drivers."""

  # This is the name the user sets
  name = ndb.StringProperty(required=False)

  # This is the (optional) name read from the device itself
  device_name = ndb.StringProperty(required=False)

  last_update = ndb.DateTimeProperty(required=False, auto_now=True)
  room = ndb.StringProperty()

  # What can I do with this device? ie SWITCH, DIMMABLE, COLOR_TEMP etc
  capabilities = ndb.ComputedProperty(lambda self: self.get_capabilities(),
                                      repeated=True)

  # What broad category does this device belong to?  LIGHTING, CLIMATE, MUSIC
  categories = ndb.ComputedProperty(lambda self: self.get_categories(),
                                    repeated=True)

  def get_capabilities(self):
    return []

  def get_categories(self):
    return []

  @classmethod
  def _event_classname(cls):
    return 'device'

  def handle_event(self, event):
    pass

  @classmethod
  def handle_static_event(cls, event):
    pass

  @classmethod
  def get_by_capability(cls, capability):
    return cls.query(Device.capabilities == capability)

  def find_room(self):
    """Resolve the room for this device.  May return null."""
    if not self.room:
      return None

    # This is a horrible hack, but room imports devices,
    # so need to be lazy here.
    from appengine import room
    room_obj = room.Room.get_by_id(self._device.room)
    if not room_obj:
      return None

    return room_obj


class DetectorMixin(object):
  detector = ndb.JsonProperty()

  def is_occupied(self):
    """Use a failure detector to determine state of sensor"""
    if self.detector is None:
      instance = detector.AccrualFailureDetector()
    else:
      instance = detector.AccrualFailureDetector.from_dict(self.detector)

    # As we don't get heart beats from the motion sensors,
    # we just fake them.
    if self.occupied:
      instance.heartbeat()

    self.detector = instance.to_dict()

    return instance.is_alive()


class Switch(Device):
  """A switch."""
  state = ndb.BooleanProperty()

  def get_capabilities(self):
    return ['SWITCH']

  def get_categories(self):
    return ['LIGHTING']


# pylint: disable=invalid-name
blueprint = flask.Blueprint('device', __name__)
rest.register_class(blueprint, Device, create_device)


def process_events(events):
  """Process a set of events."""

  device_cache = {}

  for event in events:
    device_type = event['device_type']
    device_id = event['device_id']
    event_body = event['event']

    if device_id is None:
      DEVICE_TYPES[device_type].handle_static_event(event_body)
      continue

    if device_id in device_cache:
      device = device_cache[device_id]
    else:
      device = Device.get_by_id(device_id)
      if not device:
        device = create_device(device_id, None,
                               device_type=device_type)
      device_cache[device_id] = device

    device.handle_event(event_body)

  ndb.put_multi(device_cache.values())


@blueprint.route('/events', methods=['POST'])
def handle_events():
  """Handle events from devices."""

  # This endpoint needs to authenticate itself.
  proxy = pushrpc.authenticate()
  if proxy is None:
    flask.abort(401)

  # If proxy hasn't been claimed, not much we can do.
  if proxy.building_id is None:
    logging.info('Dropping events as this proxy is not claimed')
    return ('', 204)

  # We need to set namespace - not done by main.py
  namespace_manager.set_namespace(proxy.building_id)

  events = flask.request.get_json()
  logging.info('Processing %d events', len(events))

  process_events(events)

  return ('', 204)


