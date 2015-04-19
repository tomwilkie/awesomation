"""Main entry point for code running on the raspberry pi."""

import argparse
import logging
import sys

from pi import daemon, events, hue, pushrpc, sonos, wemo


LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'
PIDFILE = '/var/run/control.pid'


class Control(object):
  """'Controller class, ties proxies and rpc together."""

  def __init__(self, args, send_event):
    self._args = args
    self._proxies = {}
    self._send_event = send_event

  def start(self):
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

    try:
      from pi import network
      self._proxies['network'] = network.NetworkMonitor(
          self._device_event_callback,
          self._args.network_scan_interval_secs,
          self._args.network_scan_timeout_secs)
    except:
      logging.debug('Exception was:', exc_info=sys.exc_info())
      logging.error('Failed to initialize network module - did you '
                    'run as root?')

    # This module needs a 433Mhz transmitter, wiringPi etc, so might not work
    try:
      from pi import rfswitch
      self._proxies['rfswitch'] = rfswitch.RFSwitch(self._args.rfswtich_pin)
    except:
      logging.debug('Exception was:', exc_info=sys.exc_info())
      logging.error('Failed to initialize rfswitch module - have you '
                    'installed rcswitch?')

    # This module needs a zwave usb stick
    try:
      from pi import zwave
      self._proxies['zwave'] = zwave.ZWave(
          self._args.zwave_device, self._device_event_callback)
    except:
      logging.debug('Exception was:', exc_info=sys.exc_info())
      logging.error('Failed to initialize zwave module - have you '
                    'installed libopenzwave?')

  def stop(self):
    for proxy in self._proxies.itervalues():
      proxy.stop()

    for proxy in self._proxies.itervalues():
      proxy.join()

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
    self._send_event(event)
