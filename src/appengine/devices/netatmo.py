"""Integration with nest devices."""

import logging
import urllib

from google.appengine.ext import ndb

from appengine import account, device, rest


@device.register('netatmo_weather_station')
class NetatmoWeatherStation(device.Device):
  """A Netatmo Weather Station."""
  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()
  co2 = ndb.FloatProperty()
  pressure = ndb.FloatProperty()
  noise = ndb.FloatProperty()

  def get_categories(self):
    return ['CLIMATE']

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

  def __init__(self, *args, **kwargs):
    super(NetatmoAccount, self).__init__(*args, **kwargs)

    # pylint: disable=invalid-name
    from common import creds
    self.CLIENT_ID = creds.NETATMO_CLIENT_ID
    self.CLIENT_SECRET = creds.NETATMO_CLIENT_SECRET

  def get_human_type(self):
    return 'Netatmo'

  def _get_refresh_data(self):
    values = {'client_id': self.CLIENT_ID,
              'client_secret': self.CLIENT_SECRET}

    if self.refresh_token is None:
      values['grant_type'] = 'authorization_code'
      values['code'] = self.auth_code
      values['redirect_uri'] = account.REDIRECT_URL
      values['scope'] = self.SCOPES
    else:
      values['grant_type'] = 'refresh_token'
      values['refresh_token'] = self.refresh_token

    return urllib.urlencode(values)

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    result = self.do_request(self.API_URL)

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

    device.process_events(events)
