"""Wemo proxy code."""

import logging
import sys
import threading

#from wemo import upnp

class Wemo(object):
  """Hue proxy object."""

  def __init__(self, refresh_period, callback):
    self._refresh_period = refresh_period
    self._callback = callback

  def _wemo_callback(self, address, headers):
    logging.info('%s, %s', address, headers)

  def _set_light(self, message):
    """Turn a light on or off."""
    bridge_id = str(message["bridge_id"])
    device_id = int(message["device_id"])
    mode = message["mode"]

    logging.info('bridge_id = %s, device_id = %s, mode = %s',
                 bridge_id, device_id, mode)

    bridge = self._bridges.get(bridge_id, None)
    light = bridge[device_id]
    light.on = mode

  def handle_events(self, messages):
    """Handle hue events - turn it on or off."""
    for message in messages:
      command = message.pop('command')

      if command == 'light':
        self._set_light(message)
      elif command == 'scan':
        self._trigger_bridge_scan()
      else:
        logging.info('Unhandled message type \'%s\'', command)

  def stop(self):
    pass
