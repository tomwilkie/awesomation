"""Integration with nest devices."""

import json
import logging

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from appengine import account, device, rest
from common import creds


@device.register('nest_thermostat')
class NestThermostat(device.Device):
  """Class represents a Nest thermostat."""
  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()
  account = ndb.StringProperty()
  target_temperature = ndb.FloatProperty()

  def get_categories(self):
    return ['CLIMATE']

  def handle_event(self, event):
    self.account = event['account']
    self.humidity = event['humidity']
    self.temperature = event['ambient_temperature_c']
    self.device_name = event['name_long']
    self.target_temperature = event['target_temperature_c']


@device.register('nest_protect')
class NestProtect(device.Device):
  """Class represents a Nest protect (smoke alarm)."""
  account = ndb.StringProperty()

  def get_categories(self):
    return ['CLIMATE']

  def handle_event(self, event):
    self.account = event['account']
    self.device_name = event['name_long']


@account.register('nest')
class NestAccount(account.Account):
  """Class represents a Nest account."""
  AUTH_URL = ('https://home.nest.com/login/oauth2?'
              'client_id=%(client_id)s&state=%(state)s')
  ACCESS_TOKEN_URL = ('https://api.home.nest.com/oauth2/access_token?'
                      'client_id=%(client_id)s&code=%(auth_code)s&'
                      'client_secret=%(client_secret)s&'
                      'grant_type=authorization_code')
  API_URL = 'https://developer-api.nest.com/devices.json?auth=%(access_token)s'
  STRUCTURES_URL = ('https://developer-api.nest.com/structures.json'
                    '?auth=%(access_token)s')
  SINGLE_STRUCTURE_URL = ('https://developer-api.nest.com/structures/'
                          '%(id)s?auth=%(access_token)s')
  CLIENT_ID = creds.NEST_CLIENT_ID
  CLIENT_SECRET = creds.NEST_CLIENT_SECRET

  def get_human_type(self):
    return 'Nest'

  def set_away(self, value):
    """Set away status of all structures."""
    structures = self.do_request(self.STRUCTURES_URL)

    logging.info(structures)
    value = 'away' if value else 'home'

    for structure_id in structures.iterkeys():
      url = self.SINGLE_STRUCTURE_URL % {'id': structure_id,
                                         'access_token': self.access_token}
      request_data = json.dumps({'away': value})
      logging.info('Sending request "%s" to %s', request_data, url)

      self.do_request(
          url, payload=request_data,
          method=urlfetch.PUT)

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    result = self.do_request(self.API_URL)
    logging.info(result)

    events = []

    if 'smoke_co_alarms' in result:
      for protect_id, protect_info in result['smoke_co_alarms'].iteritems():
        protect_info['account'] = self.key.string_id()
        events.append({
            'device_type': 'nest_protect',
            'device_id': 'nest-protect-%s' % protect_id,
            'event': protect_info,
        })

    if 'thermostats' in result:
      for thermostat_id, thermostat_info in result['thermostats'].iteritems():
        thermostat_info['account'] = self.key.string_id()
        events.append({
            'device_type': 'nest_thermostat',
            'device_id': 'nest-thermostat-%s' % thermostat_id,
            'event': thermostat_info,
        })

    device.process_events(events)
