"""Integration with insteon devices."""

import json
import logging
import sys
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from appengine import account, device, rest


@device.register('insteon_switch')
class InsteonSwitch(device.Device):
  """Class represents a Insteon switch."""
  account = ndb.StringProperty()

  def get_categories(self):
    return []

  def handle_event(self, event):
    self.account = event['account']


@account.register('insteon')
class InsteonAccount(account.Account):
  """Class represents a Insteon account."""
  BASE_URL = 'https://connect.insteon.com/api/v2'
  AUTH_URL = (BASE_URL + '/oauth2/auth?client_id=%(client_id)s&state=%(state)s&'
              'response_type=code&redirect_uri=' + account.REDIRECT_URL)
  ACCESS_TOKEN_URL = (BASE_URL + '/oauth2/token')

  def __init__(self, *args, **kwargs):
    super(InsteonAccount, self).__init__(*args, **kwargs)

    # pylint: disable=invalid-name
    from common import creds
    self.CLIENT_ID = creds.INSTEON_CLIENT_ID
    self.CLIENT_SECRET = creds.INSTEON_CLIENT_SECRET

  def _get_refresh_data(self):
    values = {'client_id': self.CLIENT_ID,
              'client_secret': self.CLIENT_SECRET}

    if self.refresh_token is None:
      values['grant_type'] = 'authorization_code'
      values['code'] = self.auth_code
      values['redirect_uri'] = '' # Don't provide a redirect, or you'll get a 401
    else:
      values['grant_type'] = 'refresh_token'
      values['refresh_token'] = self.refresh_token

    return urllib.urlencode(values)

  def get_human_type(self):
    return 'Insteon'

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    #result = self.do_request(self.API_URL)
    #logging.info(result)
    #
    #events = []
    #
    #if 'smoke_co_alarms' in result:
    #  for protect_id, protect_info in result['smoke_co_alarms'].iteritems():
    #    protect_info['account'] = self.key.string_id()
    #    events.append({
    #        'device_type': 'nest_protect',
    #        'device_id': 'nest-protect-%s' % protect_id,
    #        'event': protect_info,
    #    })
    #
    #if 'thermostats' in result:
    #  for thermostat_id, thermostat_info in result['thermostats'].iteritems():
    #    thermostat_info['account'] = self.key.string_id()
    #    events.append({
    #        'device_type': 'nest_thermostat',
    #        'device_id': 'nest-thermostat-%s' % thermostat_id,
    #        'event': thermostat_info,
    #    })
    #
    #device.process_events(events)
