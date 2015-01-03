"""Handle user related queries."""
import uuid

from google.appengine.api import channel
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import ndb

import flask

from appengine import model


# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


class Person(model.Base):
  # key_name is userid
  email = ndb.StringProperty(required=False)
  channel_tokens = ndb.StringProperty(repeated=True)


def get_user_from_namespace():
  return namespace_manager.get_namespace()


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
  user_id = get_user()
  person = Person.get_by_id(user_id)

  channel_id = str(uuid.uuid4())
  person.channel_tokens.append(channel_id)
  person.put()

  channel_token = channel.create_channel(channel_id)
  return flask.jsonify(token=channel_token)
