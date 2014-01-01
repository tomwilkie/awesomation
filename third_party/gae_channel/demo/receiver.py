""" Simple example of how to use gae channel client"""
import sys
sys.path.append('../')
import urllib2, logging
import gae_channel

def main():
    # this is the application name of the demo server
    app_name = 'channel-client-demo'
    # this could be anything unique - we just use a random string here
    channel_name = gae_channel.random_string(10)
    token = fetch_token(app_name, channel_name)
    print "Your channel name is: %s" % channel_name
    print "now run in an other terminal:"
    print "python sender.py %s" % channel_name
    listen(token)

def fetch_token(app_name, channel_name):
    """ get a channel token from demo server """

    url = "http://%s.appspot.com/channel/%s" % (app_name, channel_name)
    req = urllib2.urlopen(url)
    token = req.read()
    return token

def listen(token):
    """ just print any messages received"""
    print "I'm now listening for messages, dont close this terminal..."
    chan = gae_channel.Client(token)
    chan.logger.setLevel(logging.DEBUG)
    for msg in chan.messages():
        print "Message received: %s" % msg


if __name__ == '__main__':
    main()
