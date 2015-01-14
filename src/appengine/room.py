"""ROOMs"""
import datetime
import logging

from google.appengine.ext import ndb

import flask

from appengine import device, model, rest


class Room(model.Base):
  """A room in a property."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)

  # automatically dim lights in this room?
  auto_dim_lights = ndb.BooleanProperty(default=False)
  target_brightness = ndb.IntegerProperty()
  target_color_temperature = ndb.IntegerProperty()
  dim_start_time = ndb.IntegerProperty() # seconds from midnight
  dim_end_time = ndb.IntegerProperty() # seconds from midnight

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
  def update_auto_dim(self):
    """If this room is setup for auto dimming, then do it."""

    if self.auto_dim_lights != True:
      return

    if (self.target_brightness is None or
        self.target_color_temperature is None or
        self.dim_start_time is None or
        self.dim_end_time is None):
      logging.error('Something is None')
      return

    if self.dim_start_time > self.dim_end_time:
      logging.error('Start after end')
      return

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (now - midnight).seconds

    lights = (device.Device.get_by_capability('DIMMABLE')
              .filter(device.Device.room == self.key.string_id()).iter())

    def interpolate(target_value, max_value):
      """Given current seconds since midnight, interpolate
         between max_value and target_value."""
      if seconds_since_midnight < self.dim_start_time:
        return max_value

      if seconds_since_midnight > self.dim_end_time:
        return self.target_brightness

      value_range = max_value - target_value
      time_range = self.dim_end_time - self.dim_start_time
      time_elapsed = seconds_since_midnight - self.dim_start_time
      return max_value - ((value_range * time_elapsed) / time_range)

    brightness = interpolate(self.target_brightness, 255)
    color_temperature = interpolate(self.target_color_temperature, 500)

    logging.info('Setting brightness to %d, color temp to %d in room %s',
                 brightness, color_temperature, self.name)

    for light in lights:
      light.brightness = brightness
      if 'COLOR_TEMPERATURE' in light.capabilities:
        light.color_temperature = color_temperature
      light.sync()

    ndb.put_multi(lights)

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
