"""Base classes for my data model."""

import functools
import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

import flask


class Base(polymodel.PolyModel):

  def to_dict(self):
    """Convert this object to a python dict."""
    result = super(Base, self).to_dict()
    result['id'] = self.key.id()
    result['class'] = result['class_'][-1]
    del result['class_']
    return result


class Person(Base):
  # key_name is userid
  email = ndb.StringProperty(required=False)


class Account(Base):
  owner = ndb.StringProperty(required=True)
  oauth_state = ndb.StringProperty(required=False)
  oauth_access_token = ndb.StringProperty(required=False)
  oauth_refresh_token = ndb.StringProperty(required=False)


class Command(object):
  """Device command decorator - automatically dispatches methods."""

  def __init__(self, wrapped):
    self.wrapped = wrapped
    functools.update_wrapper(self, wrapped)

  def __call__(self, *args, **kwargs):
    return self.wrapped(*args, **kwargs)


class Device(Base):
  """Base class for all device drivers."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  last_update = ndb.DateTimeProperty(required=False, auto_now=True)

  def handle_event(self, event):
    pass

  def handle_command(self, command):
    """Dispatch command to appropriate handler."""
    logging.info(command)
    func_name = command.get('command', None)
    func = getattr(self, func_name, None)
    if func is None or not isinstance(func, Command):
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)
    func(self)

  def get_id(self):
    return self.key.string_id().split('-', 1)[1]

  def to_dict(self):
    result = Base.to_dict(self)
    result['id'] = self.get_id()
    return result


class Switch(Device):
  """A swtich."""
  state = ndb.BooleanProperty()

  @Command
  def turn_on(self):
    pass

  @Command
  def turn_off(self):
    pass
