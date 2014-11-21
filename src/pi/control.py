#!/usr/bin/python

import argparse
import json
import logging
import rcswitch
import sys
import time
import traceback
import urllib2

from common import creds
from pusherclient import Pusher
import libopenzwave

PIN=3

def Pusher():
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


def ZWaveMain(device):
  config_path = libopenzwave.configPath()
  user_path = '.'
  cmd_line = ''
  options = libopenzwave.PyOptions(config_path, user_path, cmd_line)
  options.lock()
  
  def Callback(ars):
    print args
  
  manager = libopenzwave.PyManager()
  manager.create()
  manager.addWatcher(Callback)
  manager.addDriver(device)
  
  while True:
    time.sleep(100)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('zwave_device', default='/dev/ttyUSB0')
  args = parser.parse_args()

  ZWaveMain(args.zwave_device)


if __name__ == '__main__':
    main()
