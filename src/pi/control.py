"""Main entry point for code running on the raspberry pi."""

import argparse
import collections
import logging
import time

from pi import hue, pushrpc, rfswitch, wemo_proxy, zwave


LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'


class Control(object):
  """'Controller class, ties proxies and rpc together."""

  def __init__(self, args):
    self._proxies = {
        'rfswitch': rfswitch.RFSwitch(args.rfswtich_pin),
        'zwave': zwave.ZWave(args.zwave_device, self._device_event_callback),
        'hue': hue.Hue(args.hue_scan_interval_secs,
                       self._device_event_callback),
        'wemo': wemo_proxy.Wemo(args.hue_scan_interval_secs,
                                self._device_event_callback)
    }

    self._pusher = pushrpc.PushRPC(self._push_event_callback)

  def stop(self):
    self._pusher.stop()

    for proxy in self._proxies.itervalues():
      proxy.stop()

  def _push_event_callback(self, events):
    """Handle event from the cloud."""
    logging.info('Processing %d events', len(events))

    events_by_type = collections.defaultdict(list)
    for event in events:
      events_by_type[event.pop('type')].append(event)

    for event_type, events in events_by_type.iteritems():
      if event_type not in self._proxies:
        logging.error('Event type \'%s\' unrecognised', event_type)
        continue

      self._proxies[event_type].handle_events(events)


  def _device_event_callback(self, device_type, device_id, event_body):
    """Handle event from a device."""
    event = {'device_type': device_type, 'device_id': device_id,
              'event': event_body}
    self._pusher.send_event(event)


def main():
  """Main function."""
  logging.basicConfig(format=LOGFMT, level=logging.INFO)
  file_handler = logging.FileHandler('control.log')
  file_handler.setFormatter(logging.Formatter(LOGFMT))
  logging.getLogger().addHandler(file_handler)

  parser = argparse.ArgumentParser()
  parser.add_argument('--zwave_device', default='/dev/ttyUSB0')
  parser.add_argument('--rfswtich_pin', default=3)
  parser.add_argument('--hue_scan_interval_secs', default=5*60)
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
