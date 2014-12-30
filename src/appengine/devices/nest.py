"""Integration with nest devices."""

import json
import logging
import urllib2

from google.appengine.ext import ndb

import flask

from appengine import device
from common import creds


AUTH_URL = ('https://home.nest.com/login/oauth2?client_id=%s&state=STATE'
            % creds.NEST_CLIENT_ID)
ACCESS_TOKEN_URL = ('https://api.home.nest.com/oauth2/access_token?'
                    'client_id=%(client_id)s&code=%(auth_code)s&'
                    'client_secret=%(client_secret)s&'
                    'grant_type=authorization_code')


class NestAccount(ndb.Model):
  auth_code = ndb.StringProperty(required=True)
  access_token = ndb.StringProperty(required=False)


def refresh_access_token(account):
  """For a given account, refresh the access token."""
  parameters = {'client_id': creds.NEST_CLIENT_ID,
                'auth_code': account.auth_code,
                'client_secret': creds.NEST_CLIENT_SECRET}
  url = ACCESS_TOKEN_URL % parameters
  logging.info(url)
  # empty data to trigger a post
  result = urllib2.urlopen(url, '')
  result = json.load(result)
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

  # Step 2: Nest server redirects back to us
  # with a auth_code - use this to create new
  # nest account object
  account = NestAccount(auth_code=auth_code)
  refresh_access_token(account)

  account.put()
  return "OK"
