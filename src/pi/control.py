#!/usr/bin/python

import argparse
import json
import logging
import sys
import time
import traceback
import urllib2

from pi import pushrpc, rf433, zwave


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--zwave_device', default='/dev/ttyUSB0')
  parser.add_argument('--rf433_pin', default=3)
  args = parser.parse_args()

  proxies = []
  proxies.append(rf433.RF433(args.rf433_pin))
  proxies.append(zwave.ZWave(args.zwave_device))
  
  pushrpc.Start()


if __name__ == '__main__':
    main()
