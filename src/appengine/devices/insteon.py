"""Integration with insteon devices."""

import json
import logging
import urllib
import time

from appengine import model, account, device, rest


@device.register('insteon_switch')
class InsteonSwitch(device.Switch):
  """Class represents a Insteon switch."""
  insteon_device_id = model.Property()

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

    command = 'fast_on' if self.state else 'fast_off'
    command = my_account.send_command(command, device_id=self.insteon_device_id)
    logging.info(command)


@account.register('insteon')
class InsteonAccount(account.Account):
  """Class represents a Insteon account."""
  BASE_URL = 'https://connect.insteon.com'
  AUTH_URL = (BASE_URL + '/api/v2/oauth2/auth?' +
              'client_id=%(client_id)s&state=%(state)s&'
              'response_type=code&redirect_uri=' + account.REDIRECT_URL)
  ACCESS_TOKEN_URL = (BASE_URL + '/api/v2/oauth2/token')
  COMMAND_RETRIES = 10

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

  @rest.command
  def send_command(self, command, **kwargs):
    """Utility to send commands to API."""
    if self.access_token is None:
      logging.info('No access token, can\'t send command.')
      return

    kwargs['command'] = command
    payload = json.dumps(kwargs)
    result = self.do_request(
      self.BASE_URL + '/api/v2/commands', method='POST', payload=payload,
      headers={'Content-Type': 'application/json'})
    logging.info(result)

    state = None
    for _ in range(self.COMMAND_RETRIES):
      state = self.do_request(self.BASE_URL + result['link'])
      logging.info(state)
      assert state['status'] != 'failed'
      if state['status'] == 'suceeded':
        break
      time.sleep(1)

    return state

  @rest.command
  def refresh_devices(self):
    if self.access_token is None:
      logging.info('No access token, skipping.')
      return

    devices = self.do_request(self.BASE_URL + '/api/v2/devices?properties=all')
    logging.info(devices)

    events = []
    for entry in devices['DeviceList']:
      # This covers some swtich types, will need extending for more
      if entry['DevCat'] == 2 and entry['SubCat'] in {53, 54, 55, 56, 57}:
        entry['account'] = self.id
        events.append({
            'device_type': 'insteon_switch',
            'device_id': 'insteon-%s' % entry['InsteonID'],
            'event': entry,
        })
    device.process_events(events)
