"""ROOMs"""
import datetime
import logging
import time

from google.appengine.ext import ndb

import flask

from appengine import device, model, rest


class Room(model.Base):
  """A room in a property."""
  name = ndb.StringProperty(required=False)

  # automatically dim lights in this room?
  auto_dim_lights = ndb.BooleanProperty(default=False)
  target_brightness = ndb.IntegerProperty()
  target_color_temperature = ndb.IntegerProperty()
  dim_start_time = ndb.IntegerProperty() # seconds from midnight
  dim_end_time = ndb.IntegerProperty() # seconds from midnight

  # force the lights in this room on?
  force_lights_state = ndb.BooleanProperty()
  force_lights_until = ndb.IntegerProperty()

  @classmethod
  def _event_classname(cls):
    return 'room'

  def calculate_dimming(self):
    """If this room is configured for auto dimming,
       return target brightness and color temp."""
    if self.auto_dim_lights != True:
      return None, None

    if (self.target_brightness is None or
        self.target_color_temperature is None or
        self.dim_start_time is None or
        self.dim_end_time is None):
      logging.error('  Something is None')
      return None, None

    if self.dim_start_time > self.dim_end_time:
      logging.error('  Start after end')
      return None, None

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (now - midnight).seconds

    logging.info('  start dim time = %s, end dime time = %s, '
                 'time since midnight = %s, target brightness = %d, '
                 'target color temp = %d',
                 self.dim_start_time, self.dim_end_time,
                 seconds_since_midnight, self.target_brightness,
                 self.target_color_temperature)

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

    logging.info('  setting brightness to %d, color temp to %d',
                 brightness, color_temperature)

    return (brightness, color_temperature)

  @rest.command
  def update_lights(self):
    """Update state of the lights in this room."""
    logging.info('Updating light in \'%s\'', self.name)

    # First, figure out it the room is occupied
    sensors = (device.Device.get_by_capability('OCCUPIED')
               .filter(device.Device.room == self.key.string_id()).iter())
    sensors = list(sensors)

    occupied = False
    for sensor in sensors:
      if sensor.occupied:
        occupied = True
    logging.info('  occupied = %s from %d sensors', occupied, len(sensors))

    if self.force_lights_until is not None and \
        self.force_lights_until > time.time():
      occupied = self.force_lights_state
      logging.info('  state forced to %s until %d',
                   occupied, self.force_lights_until)

    # Work out target brightness, color temperature
    target_brightness, target_color_temp = self.calculate_dimming()

    # Now iterate over all the switches and configure them
    switches = (device.Device.get_by_capability('SWITCH')
                .filter(device.Device.room == self.key.string_id()).iter())
    switches_to_put = []

    for switch in switches:
      updated = (switch.state != occupied)
      switch.state = occupied

      if (target_brightness is not None) \
          and ('DIMMABLE' in switch.capabilities):
        updated = updated or (switch.brightness != target_brightness)
        switch.brightness = target_brightness

      if (target_color_temp is not None) \
          and ('COLOR_TEMPERATURE' in switch.capabilities):
        updated = updated or (switch.color_temperature != target_color_temp)
        switch.color_temperature = target_color_temp

      if updated:
        switch.sync()
        switches_to_put.append(switch)

    if switches_to_put:
      ndb.put_multi(switches_to_put)

  @rest.command
  def all_on(self):
    self.force_lights_state = True
    self.force_lights_until = int(time.time() + 3600)
    self.update_lights()

  @rest.command
  def all_off(self):
    self.force_lights_state = False
    self.force_lights_until = int(time.time() + 3600)
    self.update_lights()


def create_room(room_id, _):
  return Room(id=room_id)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)
rest.register_class(blueprint, Room, create_room)
