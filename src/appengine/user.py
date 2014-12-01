"""Handle user related queries."""
from google.appengine.api import users
from google.appengine.ext import ndb

import flask

from appengine import model

# pylint: disable=invalid-name
blueprint = flask.Blueprint('user', __name__)


class Person(model.Base):
  # key_name is userid
  email = ndb.StringProperty(required=False)


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
