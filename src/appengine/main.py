import json

import pusher
from common import creds

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.db import polymodel 


class Device(polymodel.PolyModel):
  type = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  config = db.StringProperty(required=True)
  owner = db.StringProperty(required=True)


class NetatmoWeatherStation(Device):



class DeviceHandler(webapp.RequestHandler):
  def get(self):
    if self.request.path == "/devices/code":
      devid = self.request.get('state')
      code = self.request.get('code')
      
      response = post('https://api.netatmo.net/oauth2/token', 
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
        body = {
          grant_type: 'authorization_code',
          client_id: Netatmo.CLIENT_ID,
          client_secret: Netatmo.CLIENT_SECRET,
          code: code,
          redirect_uri: 'https://homeawesomation.appspot.com/device/access_code',
        })

      
      device = db.get(db.Key.from_path('Device', devid))



class RpcHandler(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      raise


class ChannelHandler(webapp.RequestHandler):
  def post(self, chan_name):
    event = json.loads(self.request.body)
    print event
    p = pusher.Pusher(app_id=creds.pusher_app_id, 
      key=creds.pusher_key, secret=creds.pusher_secret)
    p[chan_name].trigger('event', event)


app = webapp.WSGIApplication(
  [('/channel/(.*)', ChannelHandler),
   ('/devices/(.*)', DeviceHandler)],
  debug=True)