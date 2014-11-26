"""Base classes for my data model."""

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Base(polymodel.PolyModel):

  def to_dict(self):
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
  owner = ndb.StringProperty(required=True)
  name = ndb.StringProperty(required=False)

  def event(self, event):
    pass

  def to_dict(self):
    result = Base.to_dict(self)
    result['id'] = result['id'].split('-', 1)[1]
    return result