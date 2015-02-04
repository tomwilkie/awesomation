"""Handle user related queries."""
import collections
import logging
import re

from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import ndb

import flask
import pusher

from appengine import building, pusher_client
from common import public_creds, utils
from pi import simple_pusher


# We're not going to put these in a namespace.
class Person(ndb.Model):
  # key_name is userid
  email = ndb.StringProperty(required=False)
  buildings = ndb.StringProperty(repeated=True)

  def to_dict(self):
    """Return a dict representation of this object."""
    values = super(Person, self).to_dict()
    values['id'] = self.key.string_id()
    values['logout_url'] = users.create_logout_url('/')

    # If we are running in local mode,
    # tell the UI to connect somewhere
    # special for push updates.
    # TODO get hostname (socket doesn't work)
    if pusher_client.should_use_local():
      values['ws'] = 'ws://localhost:%d/' % (
          simple_pusher.WEBSOCKET_PORT)

    # What buildings have we shared with whom?
    values['sharing'] = collections.defaultdict(list)
    for other_person in Person.query(
        Person.buildings.IN(self.buildings)).iter():
      for other_building in other_person.buildings:
        if other_building not in self.buildings:
          continue
        values['sharing'][other_building].append(
            {'email': other_person.email,
             'user_id': other_person.key.string_id()})

    # Are there any pending invites?
    for invite in Invite.query(Invite.building.IN(
        self.buildings)).iter():
      values['sharing'][invite.building].append(
          {'email': invite.email,
           'invite_id': invite.key.id()})

    return values


# Users are keyed by this magic id we get from appengine
# we don't know this id yet, so we can't create a person
# object for them.  Instead, we'll create an invite object
# and create the person object when they first login.
class Invite(ndb.Model):
  email = ndb.StringProperty(required=False)
  building = ndb.StringProperty(repeated=False)


# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


@blueprint.before_request
def authentication():
  """Ensure user is authenticated, but don't switch namespace."""
  user_object = users.get_current_user()
  if user_object is not None:
    return

  # Special case use_invite endpoint to login.
  if flask.request.endpoint in {'user.use_invite'}:
    return flask.redirect(users.create_login_url(flask.request.url))

  flask.abort(401)

  # Intentially don't call get_person, just in case
  # this is a call to /api/invite/<id>, in which
  # case we don't want to create a new user and building.


def get_person(buildings=None):
  """Return the user_id for the current logged in user."""
  user = users.get_current_user()
  assert user is not None
  assert user.email() is not None
  assert namespace_manager.get_namespace() == ''

  # if the person is not found,
  # we'll create a new one with the
  # building id set to the user id.
  user_id = user.user_id()
  if buildings is None:
    buildings = [user_id]

  person = Person.get_or_insert(
      user_id, email=user.email(),
      buildings=buildings)
  return person


@blueprint.route('/', methods=['GET'])
def get_user_request():
  """Return the user's json."""
  assert namespace_manager.get_namespace() == ''

  person = get_person()
  values = person.to_dict()

  return flask.jsonify(objects=[values])


def send_event(building_id=None, **kwargs):
  """Post events back to the pi."""
  batch = flask.g.get('user_events', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'user_events', batch)
  if building_id is None:
    building_id = building.get_id()
  batch.append((building_id, kwargs))


def push_events():
  """Push all the events that have been caused by this request."""
  events = flask.g.get('user_events', None)
  setattr(flask.g, 'user_events', None)
  if events is None:
    return

  # partition events by building
  events_by_building = collections.defaultdict(list)
  for building_id, event in events:
    events_by_building[building_id].append(event)

  pusher_shim = pusher_client.get_client(encoder=flask.json.JSONEncoder)

  for building_id, events in events_by_building.iteritems():
    channel_id = 'private-%s' % building_id

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
  match = re.match(r'private-(\d+)', channel_name)
  building_id = match.group(1)

  if building_id not in person.buildings:
    logging.error('User %s is not allowed channel %s!',
                  person.key.string_id(), channel_name)
    flask.abort(401)

  from common import creds
  client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=public_creds.pusher_key, secret=creds.pusher_secret)
  auth = client[channel_name].authenticate(socket_id)

  return flask.jsonify(**auth)


@blueprint.route('/invite', methods=['POST'])
def invite_handler():
  """Invite a user to this building"""
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  # We know the user is authenticated at this point
  person = get_person()

  # who is the invitee?
  invitee_email = body.get('email', None)
  if invitee_email is None:
    flask.abort(400, 'Field invitee expected')

  # figure out what building we're inviting someone too
  building_id = flask.request.headers.get('building-id', person.buildings[0])
  if building_id not in person.buildings:
    flask.abort(401)

  invite = Invite(email=invitee_email, building=building_id)
  invite.put()

  app_id = app_identity.get_application_id()
  body = """
Dear %s:

An Awesomation house has been shared with you.  Visit
http://%s.appspot.com/api/user/invite/%d and sign in using your Google Account
for access.
""" % (invitee_email, app_id, invite.key.id())

  logging.info("Sending email: '%s'", body)

  mail.send_mail(
      sender=person.email, to=invitee_email,
      subject="An Awesomation house has been shared with you.",
      body=body)

  send_event(building_id=building_id, cls='user',
             id=person.key.string_id(),
             event='update', obj=person.to_dict())
  return ('', 204)


@blueprint.route('/invite/<object_id>', methods=['GET'])
def use_invite(object_id):
  """Given an invite, add the building to the current users account."""
  invite = Invite.get_by_id(int(object_id))
  if not invite:
    flask.abort(404)

  # We don't check the email on the invite, as sometimes the domain
  # doesn't match (ie @googlemail.com vs @gmail.com).  We just
  # assume if they got this code then they can have access.

  person = get_person(buildings=[invite.building])

  # There is a chance the above call didn't add the building
  # as it will only do so for people that don't alreay exist.
  # In this case, we have to add it.
  current_buildings = set(person.buildings)
  all_buildings = current_buildings | set([invite.building])
  if all_buildings != current_buildings:
    person.buildings.extend(all_buildings - current_buildings)
    person.put()

  invite.key.delete()
  return flask.redirect('/')


@blueprint.route('/invite/<object_id>', methods=['DELETE'])
def delete_invite(object_id):
  """Delete the given invite."""
  invite = Invite.get_by_id(int(object_id))
  if not invite:
    flask.abort(404)

  person = get_person()
  if invite.building not in person.buildings:
    flask.abort(401)

  invite.key.delete()

  send_event(building_id=invite.building,
             cls='user', id=person.key.string_id(),
             event='delete', obj=person.to_dict())
  return ('', 204)
