"""Philips hue proxy code."""

import logging
import sys
import threading

import requests
import phue

class Hue(object):
  """Hue proxy object."""

  def __init__(self, callback):
    self._callback = callback
    self._bridges = {}

    self._exiting = False
    self._bridge_scan_thread_condition = threading.Condition()
    self._bridge_scan_thread = threading.Thread(target=self._bridge_scan)
    self._bridge_scan_thread.daemon = True
    self._bridge_scan_thread.start()

  def _trigger_bridge_scan(self):
    with self._bridge_scan_thread_condition:
      self._bridge_scan_thread_condition.notify()

  def _bridge_scan(self):
    while not self._exiting:
      try:
        self._bridge_scan_once()
      except:
        logging.error('Error during bridge scan', exc_info=sys.exc_info())

      with self._bridge_scan_thread_condition:
        self._bridge_scan_thread_condition.wait()
        if self._exiting:
          return

  def _bridge_scan_once(self):
    """Find hue hubs on the network and tell appengine about them."""
    # pylint: disable=bare-except
    logging.info('Starting hue bridge scan')
    response = requests.get('https://www.meethue.com/api/nupnp')
    assert response.status_code == 200, response.status_code
    bridges = response.json()
    for bridge in bridges:
      bridge_id = bridge['id']
      bridge_ip = bridge['internalipaddress']
      bridge_name = bridge['name']

      # Event explicity doesn't contain ip (it might change)
      # or id (its in the device path)
      event = {'name': bridge_name}
      try:
        self._bridges[bridge_id] = phue.Bridge(ip=bridge_ip)
        event['linked'] = True
      except phue.PhueRegistrationException:
        event['linked'] = False

      logging.info('Hue bridge \'%s\' (%s) found at %s - linked=%s',
                   bridge_name, bridge_id, bridge_ip, event['linked'])

      self._callback('hue_bridge', 'hue-%s' % bridge_id, event)


  def _set_light(self, message):
    """Turn a light on or off."""
    bridge_id = str(message["bridge_id"])
    device_id = int(message["device_id"])
    mode = message["mode"]

    logging.info('bridge_id = %s, device_id = %s, mode = %s',
                  bridge_id, device_id, mode)

    bridge = self._bridges.get(bridge_id, None)
    light = bridge[device_id]
    if mode:
      light.on()
    else:
      light.off()

  def handle_event(self, message):
    """Handle hue events - turn it on or off."""
    command = message.pop('command')

    if command == 'light':
      self._set_light(message)
    elif command == 'scan':
      self._trigger_bridge_scan()
    else:
      logging.info('Unhandled message type \'%s\'', message_type)

  def stop(self):
    self._exiting = True
    self._trigger_bridge_scan()
    self._bridge_scan_thread.join()
