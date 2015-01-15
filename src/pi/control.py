"""Main entry point for code running on the raspberry pi."""

import argparse
import logging
import sys
import time

from pi import daemon, hue, network, pushrpc, rfswitch, sonos, wemo, zwave


LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'
PIDFILE = '/var/run/control.pid'


class Control(daemon.Daemon):
  """'Controller class, ties proxies and rpc together."""

  def __init__(self, args):
    super(Control, self).__init__(PIDFILE, daemonize=args.daemonize)
    self._args = args
    self._pusher = None
    self._proxies = {}

  def run(self):
    self._pusher = pushrpc.PushRPC(self._push_event_callback)

    # These modules should work 100% of the time -
    # they don't need special hardware, or root
    self._proxies = {
        'hue': hue.Hue(self._args.hue_scan_interval_secs,
                       self._device_event_callback),
        'wemo': wemo.Wemo(self._args.hue_scan_interval_secs,
                          self._device_event_callback),
        'sonos': sonos.Sonos(self._args.hue_scan_interval_secs,
                             self._device_event_callback),
    }

    # This module needs root, so might not work
    try:
      self._proxies['network'] = network.NetworkMonitor(
          self._device_event_callback,
          self._args.network_scan_interval_secs,
          self._args.network_scan_timeout_secs)
    except:
      logging.error('Failed to initialize network module',
                    exc_info=sys.exc_info())

    # This module needs root, so might not work
    try:
      self._proxies['rfswitch'] = rfswitch.RFSwitch(self._args.rfswtich_pin)
    except:
      logging.error('Failed to initialize rfswitch module',
                    exc_info=sys.exc_info())

    # This module needs a zwave usb stick
    try:
      self._proxies['zwave'] = zwave.ZWave(
          self._args.zwave_device, self._device_event_callback)
    except:
      logging.error('Failed to initialize zwave module',
                    exc_info=sys.exc_info())

    # Just sit in a loop sleeping for now
    try:
      while True:
        time.sleep(1000)
    except KeyboardInterrupt:
      logging.info('Shutting down')

    # Now try and shut everything down gracefully
    self._pusher.stop()

    for proxy in self._proxies.itervalues():
      proxy.stop()

  def _push_event_callback(self, commands):
    """Handle event from the cloud."""
    logging.info('Processing %d commands', len(commands))

    for command in commands:
      command_type = command.pop('type', None)
      proxy = self._proxies.get(command_type, None)
      if proxy is None:
        logging.error('Proxy type \'%s\' unrecognised', command_type)

      try:
        proxy.handle_command(command)
      except:
        logging.error('Error handling command.', exc_info=sys.exc_info())

  def _device_event_callback(self, device_type, device_id, event_body):
    """Handle event from a device."""
    event = {'device_type': device_type, 'device_id': device_id,
             'event': event_body}
    self._pusher.send_event(event)


def main():
  """Main function."""
  # Setup logging
  logging.basicConfig(format=LOGFMT, level=logging.INFO)
  file_handler = logging.FileHandler('control.log')
  file_handler.setFormatter(logging.Formatter(LOGFMT))
  logging.getLogger().addHandler(file_handler)
  logging.getLogger('requests.packages.urllib3.connectionpool'
      ).setLevel(logging.ERROR)

  # Command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--daemonize', dest='daemonize', action='store_true')
  parser.add_argument('--nodaemonize', dest='daemonize', action='store_false')
  parser.set_defaults(daemonize=True)

  parser.add_argument('--zwave_device',
                      default='/dev/ttyUSB0')
  parser.add_argument('--rfswtich_pin',
                      default=3)
  parser.add_argument('--hue_scan_interval_secs',
                      default=5*60)
  parser.add_argument('--network_scan_interval_secs',
                      default=10)
  parser.add_argument('--network_scan_timeout_secs',
                      default=5*60)
  parser.add_argument('action', nargs=1, choices=['start', 'stop', 'restart'],
                      metavar='<action>')
  args = parser.parse_args()

  control = Control(args)

  if args.action[0] == 'start':
    control.start()
  elif args.action[0] == 'stop':
    control.stop()
  elif args.action[0] == 'restart':
    control.restart()
  else:
    assert False, args.action


if __name__ == '__main__':
  main()
