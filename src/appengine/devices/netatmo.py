"""Integration with nest devices."""

import json
import logging
import urllib
import urllib2

from google.appengine.ext import ndb

from appengine import account, device, rest, user
from common import creds


@device.register('netatmo_weather_station')
class NetatmoWeatherStation(device.Device):
  """A Netatmo Weather Station."""
  account = ndb.StringProperty()

  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()
  co2 = ndb.FloatProperty()
  pressure = ndb.FloatProperty()
  noise = ndb.FloatProperty()

  def handle_event(self, event):
    self.device_name = event['module_name']
    self.account = event['account']

    self.temperature = event['dashboard_data'].get('Temperature', None)
    self.humidity = event['dashboard_data'].get('Humidity', None)
    self.co2 = event['dashboard_data'].get('CO2', None)
    self.pressure = event['dashboard_data'].get('Pressure', None)
    self.noise = event['dashboard_data'].get('Noise', None)


@account.register('netatmo')
class NetatmoAccount(account.Account):
  """Class represents a Netatmo account."""
  AUTH_URL = ('https://api.netatmo.net/oauth2/authorize?'
              'client_id=%(client_id)s&state=%(state)s')
  ACCESS_TOKEN_URL = 'https://api.netatmo.net/oauth2/token'
  SCOPES = 'read_station read_thermostat write_thermostat'
  API_URL = ('https://api.netatmo.net/api/devicelist?'
             'access_token=%(access_token)s')

  CLIENT_ID = creds.NETATMO_CLIENT_ID
  CLIENT_SECRET = creds.NETATMO_CLIENT_SECRET

  def get_human_type(self):
    return 'Netatmo'

  def _get_refresh_data(self):
    return urllib.urlencode({'grant_type': 'authorization_code',
                             'client_id': self.CLIENT_ID,
                             'client_secret': self.CLIENT_SECRET,
                             'code': self.auth_code,
                             'redirect_uri': account.REDIRECT_URL,
                             'scope': self.SCOPES})

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    url = self.API_URL % {'access_token': self.access_token}
    result = urllib2.urlopen(url)
    result = json.load(result)

    events = []
    for details in result['body']['modules']:
      if details['type'] not in {'NAModule1', 'NAModule4'}:
        continue

      details['account'] = self.key.string_id()
      events.append({
        'device_type': 'netatmo_weather_station',
        'device_id': 'netatmo-%s' % details['_id'],
        'event': details,
      })

    for details in result['body']['devices']:
      if details['type'] not in {'NAMain'}:
        continue

      details['account'] = self.key.string_id()
      events.append({
        'device_type': 'netatmo_weather_station',
        'device_id': 'netatmo-%s' % details['_id'],
        'event': details,
      })

    user_id = user.get_user_from_namespace()
    device.process_events(events, user_id)
