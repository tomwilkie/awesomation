import sys
import urllib2, logging
import gae_channel

def main():
    app_name = 'homeawesomation'
    channel_name = 'lights'
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
