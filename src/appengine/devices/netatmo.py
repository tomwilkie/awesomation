"""Integration with nest devices."""

import json
import logging
import urllib
import urllib2

from google.appengine.ext import ndb

from appengine import account, device, rest, user
from common import creds


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
    logging.info(result)

