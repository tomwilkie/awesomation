"""Handle user related queries."""
import logging
import re
import uuid

from google.appengine.api import channel
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import ndb

import flask


# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


class Person(ndb.Model):
  # key_name is userid
  email = ndb.StringProperty(required=False)
  channel_ids = ndb.StringProperty(repeated=True)


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
  user_id = get_user()
  person = Person.get_by_id(user_id)
  return flask.jsonify(**person.to_dict())


@blueprint.route('/new_channel')
def new_channel():
  """API for users to ask for a new channel."""
  user_id = get_user()
  person = Person.get_by_id(user_id)

  channel_id = '%s/%s' % (user_id, uuid.uuid4())
  person.channel_ids.append(channel_id)
  person.put()

  channel_token = channel.create_channel(channel_id)
  return flask.jsonify(token=channel_token)


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

  logging.info('Sending %d events to user', len(events))
  events = flask.json.dumps({'events': events})

  # Now figure out what channel to post these to.
  # Can't use user.get_user as we might not be in
  # a user's request (might be a device update
  # from the proxy).  So we use the namespace
  # instead.  Horrid.
  user_id = get_user_from_namespace()
  person = Person.get_by_id(user_id)
  if person is None:
    return

  for channel_id in person.channel_ids:
    channel.send_message(channel_id, events)


CHANNEL_REGEX = re.compile(r'^(\d+)/.*$')


def channel_connected(_):
  return ('', 204)


def channel_disconnected(channel_id):
  """Delete the channel when the UI disconnects."""
  match = CHANNEL_REGEX.match(channel_id)
  if not match:
    logging.error('"%s" not matched by channel regex.', channel_id)
    return

  user_id = match.group(1)
  namespace_manager.set_namespace(user_id)
  person = Person.get_by_id(user_id)
  if not person:
    logging.error('User %s not found!', user_id)

  person.channel_ids.remove(channel_id)
  person.put()

  return ('', 204)
