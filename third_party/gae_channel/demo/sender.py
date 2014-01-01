#!/usr/bin/python
""" Simple example of how to use gae channel client"""
import sys
import urllib2, logging, urllib

def main():
    if len(sys.argv) < 2:
        print "No channel name supplied, run receiver.py first"
        return
    while True:
        msg = raw_input("Enter a message:")
        if msg:
            send_message(msg, sys.argv[1])


def send_message(msg, channel_name):
    print "sending message: %s" % msg
    app_name = 'channel-client-demo'
    url = "http://%s.appspot.com/channel/%s" % (app_name, channel_name)
    urllib2.urlopen(url, data=urllib.urlencode({'msg': msg}))
    print "message sent"

if __name__ == '__main__':
    main()