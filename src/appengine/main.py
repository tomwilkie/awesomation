import json
import random
import string
import urllib
import urllib2

import pusher
from common import creds
import netatmo
import model

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db
from google.appengine.ext.db import polymodel 


def RandomString(length):
  return ''.join(random.choice(string.ascii_letters) for x in xrange(length))


class CreateDevice(webapp.RequestHandler):
  @login_required
  def post(self):
    user = users.get_current_user()
    device_type = self.request.get("type")
    if device_type == "netatmo.weather_station":
      device = netatmo.WeatherStation()
    else:
      assert False
    device.owner = user.user_id()
    device.put()
    self.response.out.write(json.dumps({"id": device.key}))


# First step is to create the device and redirect to do authentication
class OAuthRedirect(webapp.RequestHandler):
  @login_required
  def get(self, device_id):
    user = users.get_current_user()
    device = model.Device.get_by_id(device_id)
    assert device.owner == user.user_id()
    
    device.state = RandomString(10)
    device.put()
    
    redirect_url = "%s/device/%s/callback" % (self.request.url, device_id)
    self.redirect(device.OAUTH_AUTHORISE_URL % {
      "state": state, "client_id": device.OAUTH_CLIENT_ID, "redirect_url": redirect_url})


# One we get the callback from the service, 
class OAuthCallback(webapp.RequestHandler):
  def get(self, device_id):
    device = model.Device.get_by_id(device_id)
    state = self.request.get("state")
    assert state == device.state
    
    code = self.request.get("code")
    url = device.OAUTH_TOKEN_URL
    redirect_url = "%s/device/%s/oauth_callback" % (self.request.url, device_id)
    form_data = {
      "grant_type": "authorization_code",
      "client_id": device.CLIENT_ID,
      "client_secret": device.CLIENT_SECRET,
      "code": code,
      "redirect_uri": "",
    }
    headers = {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    params = urllib.urlencode(form_data)
    response = urllib2.urlopen(url, params)
    data = response.read()
    data = json.loads(data)
    device.access_token = data["access_token"]
    device.refresh_token = data["refresh_token"]
    device.put()


class GetUserDetails(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url())
    
    person = model.Person.get_or_insert(user.user_id())
    self.response.write(json.dumps(db.to_dict(person)))

class ChannelHandler(webapp.RequestHandler):
  def post(self, chan_name):
    event = json.loads(self.request.body)
    print event
    p = pusher.Pusher(app_id=creds.pusher_app_id, 
      key=creds.pusher_key, secret=creds.pusher_secret)
    p[chan_name].trigger('event', event)


app = webapp.WSGIApplication(
  [('/channel/(.*)', ChannelHandler),
   ('/user', GetUserDetails),
   ('/device', CreateDevice),
   ('/device/(\d+)/setup_oauth', OAuthRedirect),
   ('/device/(\d+)/oauth_callback', OAuthCallback)],
  debug=True)