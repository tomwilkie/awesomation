"""List drivers and send them commands."""
import logging

import flask

from appengine import device, rest


class Query(object):
  def iter(self):
    for name, cls in device.DEVICE_TYPES.iteritems():
      yield Driver(name, cls)


class Driver(object):
  """This is a fake for compatibility with the rest module"""

  def __init__(self, name, cls):
    self._name = name
    self._cls = cls

  def to_dict(self):
    return {'name': self._name}

  # This is a trampoline through to the driver
  # mainly for commands
  def __getattr__(self, name):
    func = getattr(self._cls, name)
    if func is None or not getattr(func, 'is_static', False):
      logging.error('Command %s does not exist or is not a static command',
                    name)
      flask.abort(400)
    return func

  @staticmethod
  def query():
    return Query()

  @staticmethod
  def get_by_id(_id):
    return Driver(_id, device.DEVICE_TYPES[_id])


# pylint: disable=invalid-name
blueprint = flask.Blueprint('driver', __name__)
rest.register_class(blueprint, Driver, None)
