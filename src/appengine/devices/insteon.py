"""Integration with insteon devices."""

import json
import logging
import urllib

from google.appengine.ext import ndb

from appengine import account, device, rest


@device.register('insteon_switch')
class InsteonSwitch(device.Switch):
  """Class represents a Insteon switch."""
  insteon_device_id = ndb.IntegerProperty()

  def handle_event(self, event):
    self.account = event['account']
    self.device_name = event['DeviceName']
    self.insteon_device_id = event['DeviceID']

  def sync(self):
    """Update the state of a light."""
    my_account = self.find_account()
    if not my_account:
      logging.info("Couldn't find account.")
      return

    command = 'on' if self.state else 'off'
    my_account.send_command(command, device_id=self.insteon_device_id)


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

  def _get_auth_headers(self):
    return {'Authentication': 'APIKey %s' % self.CLIENT_ID,
            'Authorization': 'Bearer %s' % self.access_token}

  def _get_refresh_data(self):
    values = {'client_id': self.CLIENT_ID,
              'client_secret': self.CLIENT_SECRET}

    if self.refresh_token is None:
      values['grant_type'] = 'authorization_code'
      values['code'] = self.auth_code
      # Don't provide a redirect, or you'll get a 401
      values['redirect_uri'] = ''
    else:
      values['grant_type'] = 'refresh_token'
      values['refresh_token'] = self.refresh_token

    return urllib.urlencode(values)

  def get_human_type(self):
    return 'Insteon'

  def send_command(self, command, **kwargs):
    """Utility to send commands to API."""
    if self.access_token is None:
      logging.info('No access token, can\'t send command.')
      return

    kwargs['command'] = command
    payload = json.dumps(kwargs)
    logging.info(payload)
    result = self.do_request(
      self.BASE_URL + '/commands', method='POST', payload=payload,
      headers={'Content-Type': 'application/json'})
    logging.info(result)

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    devices = self.do_request(self.BASE_URL + '/devices?properties=all')
    logging.info(devices)

    events = []
    for entry in devices['DeviceList']:
      # This covers some swtich types, will need extending for more
      if entry['DevCat'] == 2 and entry['SubCat'] in {53, 54, 55, 56, 57}:
        entry['account'] = self.key.string_id()
        events.append({
            'device_type': 'insteon_switch',
            'device_id': 'insteon-%s' % entry['InsteonID'],
            'event': entry,
        })
    device.process_events(events)
