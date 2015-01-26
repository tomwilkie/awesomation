"""Handle user related queries."""
import logging

from google.appengine.api import mail
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import ndb

import flask
import pusher

from appengine import building, pusher_client
from common import creds, public_creds, utils
from pi import simple_pusher


# We're not going to put these in a namespace.
class Person(ndb.Model):
  # key_name is userid
  email = ndb.StringProperty(required=False)
  buildings = ndb.StringProperty(repeated=True)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


@blueprint.before_request
def authentication():
  """Ensure user is authenticated, but don't switch namespace."""
  user_object = users.get_current_user()
  if not user_object:
    return flask.redirect(users.create_login_url(flask.request.url))

  # The UI will make a request to /api/user first,
  # so we look for invites here, instead of every
  # API request.
  invites = list(Invite.query(email=user_object.email()).iter())
  if not invites:
    return

  invited_buildings = {invite.building for invite in invites}

  person = get_person()
  current_buildings = set(person.building)
  all_buildings = current_buildings | invited_buildings
  if all_buildings != current_buildings:
    person.current_buildings.extend(current_buildings - all_buildings)
    person.put()

  ndb.delete_multi(invites)


def get_person():
  """Return the user_id for the current logged in user."""
  user = users.get_current_user()
  assert user is not None
  assert user.email() is not None
  assert namespace_manager.get_namespace() == ''

  user_id = user.user_id()
  person = Person.get_or_insert(
      user_id, email=user.email(),
      # if the person is not found,
      # we'll create a new one with the
      # building id set to the user id.
      buildings=[user_id])
  return person


@blueprint.route('/', methods=['GET'])
def get_user_request():
  """Return the user's json."""
  assert namespace_manager.get_namespace() == ''

  person = get_person()
  values = person.to_dict()
  values['id'] = person.key.string_id()

  # If we are running in local mode,
  # tell the UI to connect somewhere
  # special for push updates.
  # TODO get hostname (socket doesn't work)
  if pusher_client.should_use_local():
    values['ws'] = 'ws://localhost:%d/' % (
        simple_pusher.WEBSOCKET_PORT)

  return flask.jsonify(**values)


def send_event(**kwargs):
  """Post events back to the pi."""
  batch = flask.g.get('user_events', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'user_events', batch)
  building_id = building.get_id()
  batch.append((building_id, kwargs))


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
  building_id = building.get_id()
  channel_id = 'private-%s' % building_id

  # check the events are all for this building
  for _building_id, _ in events:
    assert _building_id == building_id
  events = [event for _, event in events]

  # Push them to pusher, as we've migrated
  # the UI to that.
  pusher_shim = pusher_client.get_client(encoder=flask.json.JSONEncoder)

  for batch in utils.limit_json_batch(events, max_size=8000):
    logging.info('Sending %d events to user on channel %s',
                 len(batch), channel_id)
    pusher_shim.push(channel_id, batch)


# UI calls /api/user/channel_auth with its
# (id & secret) auth and channel name == private-user_id.
# pusher client library makes a callback
# to this end point to check the client
# can use said channel.
@blueprint.route('/channel_auth', methods=['POST'])
def pusher_client_auth_callback():
  """Authenticate a given socket for a given channel."""

  # We know the user is authenticated at this point
  person = get_person()
  socket_id = flask.request.form.get('socket_id')
  channel_name = flask.request.form.get('channel_name')
  match = r'private-(\d+)'.match(channel_name)
  building_id = match.group(1)

  if building_id not in person.buildings:
    logging.error('User %s is not allowed channel %s!',
                  person.key.string_id(), channel_name)
    flask.abort(401)

  client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=public_creds.pusher_key, secret=creds.pusher_secret)
  auth = client[channel_name].authenticate(socket_id)

  return flask.jsonify(**auth)


# Users are keyed by this magic id we get from appengine
# we don't know this id yet, so we can't create a person
# object for them.  Instead, we'll create an invite object
# and create the person object when they first login.
class Invite(ndb.Model):
  email = ndb.StringProperty(required=False)
  building = ndb.StringProperty(repeated=False)


@blueprint.route('/invite', methods=['POST'])
def invite_handler():
  """Authenticate a given socket for a given channel."""
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  # We know the user is authenticated at this point
  person = get_person()

  # who is the invitee?
  invitee_email = body.get('invitee', None)
  if invitee_email is None:
    flask.abort(400, 'Field invitee expected')

  # figure out what building we're inviting someone too
  building_id = flask.request.headers.get('building-id', person.buildings[0])
  if building_id not in person.buildings:
    flask.abort(401)

  invite = Invite(email=invitee_email, building=building_id)
  invite.put()

  mail.send_mail(
      sender=person.email, to=invitee_email,
      subject="An Awesomation house has been shared with you.",
      body="""
Dear %s:

An Awesomation house has been shared with you.  Visit
http://homeawesomation.example.com/ and sign in using your Google Account
for access.
""")
