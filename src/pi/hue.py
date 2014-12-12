"""Philips hue proxy code."""

import logging
import sys
import threading

import requests
import phue

class Hue(object):
  """Hue proxy object."""

  def __init__(self, refresh_period, callback):
    self._refresh_period = refresh_period
    self._callback = callback
    self._bridges = {}
    self._lights = {}

    self._exiting = False
    self._bridge_scan_thread_condition = threading.Condition()
    self._bridge_scan_thread = threading.Thread(target=self._bridge_scan)
    self._bridge_scan_thread.daemon = True
    self._bridge_scan_thread.start()

  def _trigger_bridge_scan(self):
    with self._bridge_scan_thread_condition:
      self._bridge_scan_thread_condition.notify()

  def _bridge_scan(self):
    """Loop thread for scanning."""
    while not self._exiting:
      # We always do a scan on start up.
      try:
        self._bridge_scan_once()
      except:
        logging.error('Error during bridge scan', exc_info=sys.exc_info())

      with self._bridge_scan_thread_condition:
        self._bridge_scan_thread_condition.wait(self._refresh_period)
        if self._exiting:
          break
    logging.info('Exiting scan thread')

  def _bridge_scan_once(self):
    """Find hue hubs on the network and tell appengine about them."""
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
      event = None
      try:
        bridge = phue.Bridge(ip=bridge_ip)

        if bridge_id not in self._bridges:
          self._bridges[bridge_id] = bridge
          event = {'name': bridge_name, 'linked': True}
      except phue.PhueRegistrationException:
        if bridge_id in self._bridges:
          del self._bridges[bridge_id]
          event = {'name': bridge_name, 'linked': False}

      if event is not None:
        logging.debug('Hue bridge \'%s\' (%s) found at %s - linked=%s',
                      bridge_name, bridge_id, bridge_ip, event['linked'])

        self._callback('hue_bridge', 'hue-%s' % bridge_id, event)

    # Now find all the lights
    for bridge_id, bridge in self._bridges.iteritems():
      lights_by_id = bridge.get_light_objects(mode='id')
      for light_id in lights_by_id.iterkeys():
        light_details = bridge.get_light(light_id)
        logging.debug('Hue light %d (\'%s\') found on bridge \'%s\', on=%s',
                      light_id, light_details['name'], bridge_id,
                      light_details['state']['on'])

        light_id = 'hue-%s-%d' % (bridge_id, light_id)
        if self._lights.get(light_id, None) != light_details:
          self._callback('hue_light', light_id, light_details)
          self._lights[light_id] = light_details

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
    self._exiting = True
    self._trigger_bridge_scan()
    self._bridge_scan_thread.join()
