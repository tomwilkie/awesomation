"""Base classes for my data model."""

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


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


class Device(Base):
  """Base class for all device drivers."""
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)
  last_update = ndb.DateTimeProperty(required=False, auto_now=True)

  def handle_event(self, event):
    pass

  def handle_command(self, command):
    pass

  def get_id(self):
    return self.key.string_id().split('-', 1)[1]

  def to_dict(self):
    result = Base.to_dict(self)
    result['id'] = self.get_id()
    return result
