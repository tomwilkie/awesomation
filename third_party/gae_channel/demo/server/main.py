from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import channel

class ChannelHandler(webapp.RequestHandler):
    """ sends ping channel specified player
    """

    def get(self, chan_name):
        """ create new token"""
        token = channel.create_channel(chan_name)
        self.response.out.write(token)

    def post(self, chan_name):
        msg = self.request.get('msg')
        if msg is None:
            self.response.error(400)
            self.response.out.write('msg parameter missing')
        else:
            channel.send_message(chan_name, msg)


application = webapp.WSGIApplication([ ('/channel/(.*)', ChannelHandler),
                                      ],
                                     #(r'/player/(.*)/(.*)', BrowseHandler)],
                                     debug=True)

def main():
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
