"""Regular update task."""
import logging
import sys

from google.appengine.ext.ndb import metadata
from google.appengine.api import namespace_manager

import flask

from appengine import account, pushrpc, user


# pylint: disable=invalid-name
blueprint = flask.Blueprint('tasks', __name__)


def update_per_namespace():
  """Do a bunch of periodic stuff for a user."""
  accounts = account.Account.query().iter()
  for acc in accounts:
    try:
      acc.refresh_devices()
      acc.put()
    except:
      logging.error('Error refreshing account %s',
                    acc.key.string_id(), exc_info=sys.exc_info())

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
