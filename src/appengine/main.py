import json
import logging
import random
import string

import accounts
import model
import pusher
from common import creds

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class GetUserDetails(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    logging.debug(user)
    if user is None:
      self.redirect(users.create_login_url(self.request.path))
      return

    person = model.Person.get_or_insert(key_name=user.user_id())
    self.response.write(json.dumps(db.to_dict(person)))


class ChannelHandler(webapp.RequestHandler):
  def post(self, chan_name):
    event = json.loads(self.request.body)
    print event
    p = pusher.Pusher(app_id=creds.pusher_app_id, 
      key=creds.pusher_key, secret=creds.pusher_secret)
    p[chan_name].trigger('event', event)


app = webapp.WSGIApplication(
  [('/api/channel/(.*)', ChannelHandler),
   ('/api/user', GetUserDetails)]
   + accounts.endpoints,
  debug=True)