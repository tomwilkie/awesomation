"""Main entry point for code running on the raspberry pi."""

import argparse
import logging
import time

from pi import pushrpc, rf433, zwave


LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'


class Control(object):
  """'Controller' class, ties proxies and rpc together."""

  def __init__(self, args):
    self._proxies = {
        'rf433': rf433.RF433(args.rf433_pin),
        'zwave': zwave.ZWave(args.zwave_device, self._device_event_callback),
    }

    self._pusher = pushrpc.PushRPC(self._push_event_callback)

  def stop(self):
    self._pusher.stop()

    for proxy in self._proxies.itervalues():
      proxy.stop()

  def _push_event_callback(self, event):
    """Handle event from the cloud."""
    logging.info('Processing Event - %s', event)
    event_type = event.get('type')
    event_data = event.get('data')

    if event_type in self._proxies:
      self._proxies[event_type].handle_event(event_data)
    else:
      logging.error('Event type \'%s\' unrecognised', event_type)

  def _device_event_callback(self, driver, event):
    """Handle event from a device."""
    self._pusher.send_event((driver, event))


def main():
  """Main function."""
  logging.basicConfig(format=LOGFMT, level=logging.INFO)

  parser = argparse.ArgumentParser()
  parser.add_argument('--zwave_device', default='/dev/ttyUSB0')
  parser.add_argument('--rf433_pin', default=3)
  args = parser.parse_args()

  control = Control(args)

  try:
    while True:
      time.sleep(1000)
  except KeyboardInterrupt:
    logging.info('Shutting down')

  control.stop()


if __name__ == '__main__':
  main()
