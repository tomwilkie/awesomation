"""Handle user related queries."""
import logging

from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import ndb

import flask
import pusher

from common import creds, public_creds, utils


# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


class Person(ndb.Model):
  # key_name is userid
  email = ndb.StringProperty(required=False)


def get_user_from_namespace():
  namespace = namespace_manager.get_namespace()
  assert namespace != ''
  return namespace


def get_user():
  """Return the user_id for the current logged in user."""
  user = users.get_current_user()
  assert user is not None
  assert user.email() is not None

  person = Person.get_or_insert(
      user.user_id(), email=user.email())
  return person.key.id()


@blueprint.route('/', methods=['GET'])
def get_user_request():
  """Return the user's json."""
  user_id = get_user()
  person = Person.get_by_id(user_id)
  values = person.to_dict()
  values['id'] = user_id
  return flask.jsonify(**values)


def send_event(**kwargs):
  """Post events back to the pi."""
  batch = flask.g.get('user_events', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'user_events', batch)
  batch.append(kwargs)


def push_events():
  """Push all the events that have been caused by this request."""
  events = flask.g.get('user_events', None)
  setattr(flask.g, 'user_events', None)
  if events is None:
    return

  # Now figure out what channel to post these to.
  # Can't use user.get_user as we might not be in
  # a user's request (might be a device update
  # from the proxy).  So we use the namespace
  # instead.  Horrid.
  user_id = get_user_from_namespace()
  channel_id = 'private-%s' % user_id

  # Push them to pusher, as we've migrated
  # the UI to that.
  pusher_client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=public_creds.pusher_key,
      secret=creds.pusher_secret,
      encoder=flask.json.JSONEncoder)

  for batch in utils.limit_json_batch(events, max_size=8000):
    logging.info('Sending %d events to user on channel %s',
                 len(batch), channel_id)
    pusher_client[channel_id].trigger('events', batch)


# UI calls /api/user/channel_auth with its
# (id & secret) auth and channel name == private-user_id.
# pusher client library makes a callback
# to this end point to check the client
# can use said channel.
@blueprint.route('/channel_auth', methods=['POST'])
def pusher_client_auth_callback():
  """Authenticate a given socket for a given channel."""

  # We know the user is authenticated at this point
  user_id = get_user()
  socket_id = flask.request.form.get('socket_id')
  channel_name = flask.request.form.get('channel_name')
  if channel_name != 'private-%s' % user_id:
    logging.error('User %s is not allowed channel %s!', user_id, channel_name)
    flask.abort(401)

  pusher_client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=public_creds.pusher_key, secret=creds.pusher_secret)
  auth = pusher_client[channel_name].authenticate(socket_id)

  return flask.jsonify(**auth)
