import sys
import urllib2
import logging
import json
import time
import traceback

from common import creds
from pusherclient import Pusher

PIN=3

def main():
    pusher = Pusher(creds.pusher_key)
    switch = rcswitch.RCSwitch()
    switch.enableTransmit(PIN)

    def callback(data):
        try:
            data = json.loads(data)
            print data
            operation = 1 
            system_code = data["system_code"]
            device_code = int(data["device_code"])
            
            if data["mode"]:
              switch.switchOn(system_code, device_code)
            else:
              switch.switchOff(system_code, device_code)
            
        except Exception, e:
            print e
            traceback.print_exc()

    def connect_handler(data):
        channel = pusher.subscribe('test')
        channel.bind('event', callback)

    pusher.connection.bind('pusher:connection_established',
        connect_handler)
    pusher.connect()

    while True:
        time.sleep(100)


if __name__ == '__main__':
    main()
