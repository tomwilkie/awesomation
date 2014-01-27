from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(db.model):
  userid = db.StringProperty(required=True)
  email = db.StringProperty(required=False)

class Device(polymodel.PolyModel):
  name = db.StringProperty(required=False)
  config = db.StringProperty(required=False)
  owner = db.StringProperty(required=True)
  oauth_state = db.StringProperty(required=False)




