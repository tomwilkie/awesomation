from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Person(db.Model):
  # key_name is userid
  email = db.StringProperty(required=False)


class Account(polymodel.PolyModel):
  owner = db.StringProperty(required=True)
  oauth_state = db.StringProperty(required=False)
  oauth_access_token = db.StringProperty(required=False)
  oauth_refresh_token = db.StringProperty(required=False)


class Device(polymodel.PolyModel):
  owner = db.StringProperty(required=True)
  name = db.StringProperty(required=False)




