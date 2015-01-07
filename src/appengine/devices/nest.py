"""Integration with nest devices."""

import json
import logging
import urllib2

from google.appengine.ext import ndb

from appengine import account, device, rest, user
from common import creds


@device.register('nest_thermostat')
class NestThermostat(device.Device):
  """Class represents a Nest thermostat."""
  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()
  account = ndb.StringProperty()

  def handle_event(self, event):
    self.humidity = event['humidity']
    self.temperature = event['ambient_temperature_c']
    self.name = event['name_long']


@device.register('nest_protect')
class NestProtect(device.Device):
  """Class represents a Nest protect (smoke alarm)."""
  account = ndb.StringProperty()

  def handle_event(self, event):
    self.name = event['name_long']


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
  CLIENT_ID = creds.NEST_CLIENT_ID
  CLIENT_SECRET = creds.NEST_CLIENT_SECRET

  def get_human_type(self):
    return 'Nest'

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    url = self.API_URL % {'access_token': self.access_token}
    result = urllib2.urlopen(url)
    result = json.load(result)
    logging.info(result)

    events = []

    for protect_id, protect_info in result['smoke_co_alarms'].iteritems():
      events.append({
          'device_type': 'nest_protect',
          'device_id': 'nest-protect-%s' % protect_id,
          'event': protect_info,
      })

    for thermostat_id, thermostat_info in result['thermostats'].iteritems():
      events.append({
          'device_type': 'nest_thermostat',
          'device_id': 'nest-thermostat-%s' % thermostat_id,
          'event': thermostat_info,
      })

    user_id = user.get_user_from_namespace()
    device.process_events(events, user_id)
