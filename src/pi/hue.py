"""Philips hue proxy code."""

import logging

import requests
import phue

from pi import proxy, scanning_proxy


class Hue(scanning_proxy.ScanningProxy):
  """Hue proxy object."""

  def __init__(self, refresh_period, callback):
    super(Hue, self).__init__(refresh_period)

    self._callback = callback
    self._bridges = {}
    self._lights = {}

  def _scan_once(self):
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

  @proxy.command
  def set_state(self, bridge_id, device_id, mode,
                brightness=255, color_temperature=500):
    """Turn a light on or off."""
    logging.info('bridge_id = %s, device_id = %d, mode = %s, '
                 'brightness = %s, color temp = %s',
                 bridge_id, device_id, mode, brightness,
                 color_temperature)

    bridge = self._bridges.get(bridge_id, None)
    if not bridge:
      logging.error('Bridge %d not found!', bridge_id)

    command = {'transitiontime' : 30, 'on' : mode,
               'bri' : brightness}
    if color_temperature is not None:
      command['ct'] = color_temperature

    bridge.set_light(device_id, command)
