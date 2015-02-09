"""Code to push events to users."""
import logging

import flask
import pusher

from google.appengine.api import namespace_manager
from google.appengine.ext import ndb

from common import public_creds
from appengine import pusher_client, rest


# pylint: disable=invalid-name
blueprint = flask.Blueprint('pushrpc', __name__)


@blueprint.before_request
def before_request():
  """Requst here should use authenticated using special device code."""

  # this endpoing needs normal users
  if flask.request.endpoint in {'pushrpc.claim_proxy'}:
    rest.default_user_authentication()
    return

  # the rest in this module should be proxy-auth
  if flask.request.headers.get('awesomation-proxy', None) != 'true':
    flask.abort(401)

  proxy = authenticate()
  if proxy is None:
    flask.abort(401)


# Proxies have ids and a secret.
# The proxy authenticates with said ID and secret at
# the HTTP layer, to create a proxy object.  It then
# uses this object to create a private pusher channel.
# Events from the proxy are authenticated in the same
# way.

# Note these proxy object live in the default namespace,
# not the per-user one (so users can't see them).
class Proxy(ndb.Model):
  secret = ndb.StringProperty()
  building_id = ndb.StringProperty()


# Step 1. Create a proxy object with id & secret.
#         This happens by default on the first
#         request for unknown proxies.
def authenticate():
  """Check this request comes from a valid proxy."""
  assert namespace_manager.get_namespace() == ''

  header = flask.request.headers.get('awesomation-proxy', None)
  if header != 'true':
    logging.debug('Incorrent header for proxy auth - '
                  'awesomation-proxy = \'%s\'', header)
    return None

  if flask.request.endpoint not in {'device.handle_events',
                                    'pushrpc.pusher_client_auth_callback'}:
    logging.debug('Endpoint not allowed for proxy auth - '
                  '\'%s\'', flask.request.endpoint)
    return None

  auth = flask.request.authorization
  if not auth:
    logging.error('Proxy auth requires basic auth!')
    return None

  proxy = Proxy.get_or_insert(
      auth.username, secret=auth.password)

  # if we fetched the proxy,
  # need to check the secret.
  if proxy.secret != auth.password:
    logging.error('Incorrect secret for proxy auth!')
    return None

  return proxy


# Step 1(b). Users need to claim a proxy from the UI
@blueprint.route('/claim', methods=['POST'])
def claim_proxy():
  """Claim the given proxy id for the current user."""
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  proxy_id = body.get('proxy_id', None)
  if proxy_id is None or proxy_id == '':
    flask.abort(400, 'proxy_id required.')

  # this will run as a user, so we don't need to authenticate
  # it (already done in main).  Running in users namespace.
  assert namespace_manager.get_namespace() != ''
  building_id = namespace_manager.get_namespace()

  # We need to reset the namespace to access the proxies
  namespace_manager.set_namespace(None)
  proxy = Proxy.get_by_id(proxy_id)
  if proxy == None:
    logging.info('Proxy \'%s\' not found', proxy_id)
    flask.abort(404)

  if proxy.building_id is not None:
    flask.abort(400, 'Proxy already claimed')

  proxy.building_id = building_id
  proxy.put()
  return ('', 201)


# Step 2. Proxy call /api/proxy/channel_auth with its
#         (id & secret) auth and channel name == private-id.
#         pusher client library makes a callback
#         to this end point to check the client
#         can use said channel.
@blueprint.route('/channel_auth', methods=['GET'])
def pusher_client_auth_callback():
  """Authenticate a given socket for a given channel."""

  # Proxies use basic auth
  proxy = authenticate()
  if proxy is None:
    flask.abort(401)

  socket_id = flask.request.args.get('socket_id')
  channel_name = flask.request.args.get('channel_name')
  if channel_name != 'private-%s' % proxy.key.string_id():
    logging.error('Proxy %s is not allowed channel %s!', proxy, channel_name)
    flask.abort(401)

  # Hack, but some people won't have this (when running locally)
  from common import creds
  client = pusher.Pusher(
      app_id=creds.PUSHER_APP_ID,
      key=public_creds.pusher_key, secret=creds.PUSHER_SECRET)
  auth = client[channel_name].authenticate(socket_id)

  return flask.jsonify(**auth)


def send_event(event):
  """Post events back to the pi."""
  batch = flask.g.get('events', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'events', batch)
  batch.append(event)


def push_batch():
  """Push all the events that have been caused by this request."""
  batch = flask.g.get('events', None)
  setattr(flask.g, 'events', None)
  if batch is None:
    return

  logging.info('Sending %d events to proxy', len(batch))
  pusher_shim = pusher_client.get_client()

  # Now figure out what channel to post these to.
  # Building id should always be in the namespace
  # for any request which triggers events.
  # So we use the namespace.  Horrid.
  assert namespace_manager.get_namespace() != ''
  building_id = namespace_manager.get_namespace()

  try:
    namespace_manager.set_namespace(None)
    proxies = Proxy.query(Proxy.building_id == building_id).iter()
    for proxy in proxies:
      channel_id = 'private-%s' % proxy.key.string_id()
      logging.info('Pushing %d events to channel %s', len(batch), channel_id)
      pusher_shim.push(channel_id, batch)
  finally:
    namespace_manager.set_namespace(building_id)

