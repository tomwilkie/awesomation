"""Regular update task."""
import logging
import sys

from google.appengine.ext.ndb import metadata
from google.appengine.api import namespace_manager

import flask

from appengine import account, pushrpc, room, user


# pylint: disable=invalid-name
blueprint = flask.Blueprint('tasks', __name__)


@blueprint.before_request
def before_request():
  # Cron jobs are authenticated as a special case
  if flask.request.headers.get('X-AppEngine-Cron', None) != 'true':
    flask.abort(401)


def _update_per_namespace():
  """Do a bunch of periodic stuff for a user."""

  for acc in account.Account.query().iter():
    try:
      acc.refresh_devices()
      acc.put()
    except:
      logging.error('Error refreshing account %s',
                    acc.key.string_id(), exc_info=sys.exc_info())

  for _room in room.Room.query().iter():
    try:
      _room.update_lights()
    except:
      logging.error('Error updating room %s',
                    _room.name, exc_info=sys.exc_info())


def update_per_namespace():
  try:
    _update_per_namespace()
  except:
    logging.error('Error updating for user', exc_info=sys.exc_info())
  finally:
    pushrpc.push_batch()
    user.push_events()


@blueprint.route('/update', methods=['GET'])
def update():
  """Iterate through all the users and do stuff."""
  for namespace in metadata.get_namespaces():
    logging.info('Switching namespace: \'%s\'', namespace)
    namespace_manager.set_namespace(namespace)
    update_per_namespace()

  namespace_manager.set_namespace('')
  return ('', 204)
