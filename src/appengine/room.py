"""ROOMs"""
import datetime
import logging
import time

from google.appengine.ext import ndb

import flask

from appengine import device, model, rest

SENSOR_OVERIDE_PERIOD = 60 * 60


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
  force_lights_state = ndb.BooleanProperty(default=False)
  force_lights_at = ndb.IntegerProperty()

  # deprecated
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

      # If its before 4am, lights should be target value.
      # This stops the lights going full bright at midnight.
      if seconds_since_midnight < (4 * 3600):
        return to_value

      # Otherwise, if its before the dim start time,
      # they should be on initial value (ie bright)
      elif seconds_since_midnight < self.dim_start_time:
        return from_value

      # Finally, if its after the dimming end time,
      # should be on target value
      elif seconds_since_midnight > self.dim_end_time:
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

  def is_occupied(self):
    """Work out if this room is occupied."""
    # First, figure out if there are sensors
    sensors = (device.Device.get_by_capability('OCCUPIED')
               .filter(device.Device.room == self.key.string_id()).iter())
    sensors = list(sensors)

    # If we didn't find any, we can't tell if the room
    # is occupied
    if not sensors:
      return None, None

    # We have some sensors; if any detect movement,
    # room is occupied
    readings = []
    any_true = False
    for sensor in sensors:
      # use failure detector to decide if this sensor
      # is 'occupied'
      status = sensor.is_occupied()
      any_true |= status
      readings.append((status, sensor.inferred_last_update))

    # Either one of more have detected occupied, or none have
    # We're going to report different timestamps in each case
    if not any_true:
      # If we didn't find any, return the largest timestamp
      # ie the latest any movement was detected
      return False, max(timestamp for _, timestamp in readings)
    else:
      # If we did find some, return the return the larget timestamp
      # which is true - the earliest any movement was detected.
      return True, min(timestamp for reading, timestamp in readings if reading)

    # This model is not sufficient, as if two sensors are in the room
    # alternating status with a slight overlap, we'll report an early
    # state change.

  def resolve(self, states):
    """Resolve a list of tuples (state, time) to find the latest states.
       input does not need to be sorted."""

    def key((_, timestamp)):
      if timestamp is None:
        return 0
      return timestamp
    states.sort(key=key)
    return states[-1][0]

  @rest.command
  def update_lights(self):
    """Update state of the lights in this room."""
    logging.info('Updating light in \'%s\'', self.name)
    put_batch = []

    # The state of a given light is comprised of 3 things:
    # the indended state of the room, the state of the motion
    # sensors, and the indended state of the lights.  We use
    # simple last-writer-wins approach to device which one to use.
    states = [(self.force_lights_state, self.force_lights_at)]
    occupied, occupied_at = self.is_occupied()
    if occupied is not None:
      states.append((occupied, occupied_at))
    potential_intended_state = self.resolve(states)
    if potential_intended_state is None:
      potential_intended_state = False
    logging.info('potential_intended_state = %s, states = %s',
                 potential_intended_state, states)

    # Work out target brightness, color temperature
    target_brightness, target_color_temp = self.calculate_dimming()

    # Now iterate over all the switches and configure them
    switches = (device.Device.get_by_capability('SWITCH')
                .filter(device.Device.room == self.key.string_id()).iter())

    for switch in switches:
      if switch.intended_state is not None:
        intended_state = self.resolve(
            states + [(switch.intended_state, switch.state_last_update)])
      else:
        intended_state = potential_intended_state

      updated = (switch.state != potential_intended_state)
      switch.state = intended_state

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
        put_batch.append(switch)

    if put_batch:
      ndb.put_multi(put_batch)

  @rest.command
  def all_on(self):
    self.force_lights_state = True
    self.force_lights_at = int(time.time())
    self.update_lights()

  @rest.command
  def all_off(self):
    self.force_lights_state = False
    self.force_lights_at = int(time.time())
    self.update_lights()


def create_room(room_id, _):
  return Room(id=room_id)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('room', __name__)
rest.register_class(blueprint, Room, create_room)
