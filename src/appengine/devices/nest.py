"""Integration with nest devices."""

import json
import logging
import urllib2

from google.appengine.ext import ndb

import flask

from appengine import device, user
from common import creds


AUTH_URL = ('https://home.nest.com/login/oauth2?client_id=%s&state=STATE'
            % creds.NEST_CLIENT_ID)
ACCESS_TOKEN_URL = ('https://api.home.nest.com/oauth2/access_token?'
                    'client_id=%(client_id)s&code=%(auth_code)s&'
                    'client_secret=%(client_secret)s&'
                    'grant_type=authorization_code')
API_URL = 'https://developer-api.nest.com/devices.json?auth=%(access_token)s'


class NestThermostat(device.Device):
  """Class represents a Nest thermostat."""
  temperature = ndb.FloatProperty()
  humidity = ndb.FloatProperty()

  def update(self, info):
    self.humidity = info['humidity']
    self.temperature = info['ambient_temperature_c']
    self.name = info['name']


class NestProtect(device.Device):
  """Class represents a Nest protect (smoke alarm)."""
  def update(self, info):
    self.name = info['name']


class NestAccount(ndb.Model):
  """Class represents a Nest account."""

  auth_code = ndb.StringProperty(required=True)
  access_token = ndb.StringProperty(required=False)
  thermostats = ndb.KeyProperty(repeated=True)
  protects = ndb.KeyProperty(repeated=True)

  def refresh_devices(self):
    url = API_URL % {'access_token': self.access_token}
    result = urllib2.urlopen(url)
    result = json.load(result)
    logging.info(result)

    user_id = user.get_user()

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



def refresh_access_token(account):
  """For a given account, refresh the access token."""
  parameters = {'client_id': creds.NEST_CLIENT_ID,
                'auth_code': account.auth_code,
                'client_secret': creds.NEST_CLIENT_SECRET,
                'grant_type': 'authorization_code'}
  url = ACCESS_TOKEN_URL % parameters
  logging.info(url)

  try:
    # empty data to trigger a post
    result = urllib2.urlopen(url, '')
    result = json.load(result)
  except urllib2.HTTPError, e:
    result = json.load(e)
    logging.info(result)
    return

  assert 'access_token' in result
  account.access_token = result['access_token']


# pylint: disable=invalid-name
blueprint = flask.Blueprint('nest', __name__)


@blueprint.route('/redirect')
def nest_redirect_callback():
  # Step 1; <s>cut a hole in the box</s>
  # UI will open this page; we will redirect to
  # Nest server
  auth_code = flask.request.args.get('code')
  if auth_code is None:
    return flask.redirect(AUTH_URL)

  # Step TODO: check state in callback is unique

  # Step 2: Nest server redirects back to us
  # with a auth_code - use this to create new
  # nest account object
  account = NestAccount(auth_code=auth_code)
  refresh_access_token(account)

  account.refresh_devices()

  account.put()
  return "OK"
