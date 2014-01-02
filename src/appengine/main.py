import json

import pusher
from common import creds

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class ChannelHandler(webapp.RequestHandler):
    def post(self, chan_name):
		event = json.loads(self.request.body)
		p = pusher.Pusher(app_id=creds.pusher_app_id, 
			key=creds.pusher_key, secret=creds.pusher_secret)
		p[chan_name].trigger('event', event)


app = webapp.WSGIApplication(
	[('/channel/(.*)', ChannelHandler)],
    debug=True)