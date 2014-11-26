"""Base classes for my data model."""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Base(polymodel.PolyModel):

  def to_dict(self):
    result = db.to_dict(self)
    result['id'] = self.key().id_or_name()
    return result


class Person(Base):
  # key_name is userid
  email = db.StringProperty(required=False)


class Account(Base):
  owner = db.StringProperty(required=True)
  oauth_state = db.StringProperty(required=False)
  oauth_access_token = db.StringProperty(required=False)
  oauth_refresh_token = db.StringProperty(required=False)


class Device(Base):
  owner = db.StringProperty(required=True)
  name = db.StringProperty(required=False)

  def event(self, event):
    pass

  def to_dict(self):
    result = Base.to_dict(self)
    result['id'] = result['id'].split('-', 1)[1]
    return result