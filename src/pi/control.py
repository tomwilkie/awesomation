#!/usr/bin/python

import argparse
import logging

from pi import pushrpc, rf433, zwave


def main():
  logging.basicConfig(format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s')
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--zwave_device', default='/dev/ttyUSB0')
  parser.add_argument('--rf433_pin', default=3)
  args = parser.parse_args()

  proxies = {
    'rf433': rf433.RF433(args.rf433_pin),
    'zwave': zwave.ZWave(args.zwave_device),
  }
  
  pusher = pushrpc.PushRPC()
  
  for event in pusher.Events():
    logging.info('Processing Event - %s', event)
    event_type = event.get('type')
    event_data = event.get('data')
    
    if event_type in proxies:
      proxies[event_type].HandleEvent(event_data)
    else:
      logging.error('Event type \'%s\' unrecognised', event_type)
    
  for proxy in proxies.itervalues():
    proxy.Stop()


if __name__ == '__main__':
    main()
