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
      if switch.state != value:
        switch.state = value
        switch.sync()

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

    logging.info('%s: start dim time = %s, end dime time = %s, '
                 'time since midnight = %s, target brightness = %d, '
                 'target color temp = %d',
                 self.name, self.dim_start_time, self.dim_end_time,
                 seconds_since_midnight, self.target_brightness,
                 self.target_color_temperature)

    lights = (device.Device.get_by_capability('DIMMABLE')
              .filter(device.Device.room == self.key.string_id()).iter())
    lights = list(lights)

    def interpolate(from_value, to_value):
      """Given current seconds since midnight, interpolate
         between max_value and target_value."""
      if seconds_since_midnight < self.dim_start_time:
        return from_value

      if seconds_since_midnight > self.dim_end_time:
        return to_value

      value_range = from_value - to_value
      time_range = self.dim_end_time - self.dim_start_time
      time_elapsed = seconds_since_midnight - self.dim_start_time
      return from_value - ((value_range * time_elapsed) / time_range)

    brightness = interpolate(255, self.target_brightness)
    color_temperature = interpolate(153, self.target_color_temperature)

    logging.info('%s: setting brightness to %d, color temp to %d',
                 self.name, brightness, color_temperature)

    for light in lights:
      need_sync = False

      if light.brightness != brightness:
        light.brightness = brightness
        need_sync = True

      if 'COLOR_TEMPERATURE' in light.capabilities:
        if light.color_temperature != color_temperature:
          light.color_temperature = color_temperature
          need_sync = True

      if need_sync:
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
