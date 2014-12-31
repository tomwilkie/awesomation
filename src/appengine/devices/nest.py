"""Integration with nest devices."""

import json
import logging
import urllib2

from google.appengine.ext import ndb

from appengine import account, device, rest, user
from common import creds


class NestThermostat(device.Device):
  """Class represents a Nest thermostat."""
  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()

  def update(self, info):
    self.humidity = info['humidity']
    self.temperature = info['ambient_temperature_c']
    self.name = info['name_long']


class NestProtect(device.Device):
  """Class represents a Nest protect (smoke alarm)."""

  def update(self, info):
    self.name = info['name_long']


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

  thermostats = ndb.KeyProperty(repeated=True)
  protects = ndb.KeyProperty(repeated=True)

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    url = self.API_URL % {'access_token': self.access_token}
    result = urllib2.urlopen(url)
    result = json.load(result)
    logging.info(result)

    user_id = user.get_user_from_namespace()

    for protect_id, protect_info in result['smoke_co_alarms'].iteritems():
      key = 'nest-protect-%s' % protect_id
      if key not in self.protects:
        protect = NestProtect(id=key, owner=user_id)
        self.protects.append(protect.key)
      else:
        protect = NestProtect.get_by_id(key)

      protect.update(protect_info)
      protect.put()

    for thermostat_id, thermostat_info in result['thermostats'].iteritems():
      key = 'nest-thermostat-%s' % thermostat_id
      if key not in self.thermostats:
        thermostat = NestThermostat(id=key, owner=user_id)
        self.thermostats.append(thermostat.key)
      else:
        thermostat = NestThermostat.get_by_id(key)

      thermostat.update(thermostat_info)
      thermostat.put()

