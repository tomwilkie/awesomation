"""Regular update task."""

import logging

from google.appengine.ext.ndb import metadata
from google.appengine.api import namespace_manager

import flask

from appengine import account


# pylint: disable=invalid-name
blueprint = flask.Blueprint('tasks', __name__)


def update_per_namespace():
  """Do a bunch of periodic stuff for a user."""
  accounts = account.Account.query().iter()
  for acc in accounts:
    acc.refresh_devices()
    acc.put()


@blueprint.route('/update', methods=['GET'])
def update():
  """Iterate through all the users and do stuff."""
  for namespace in metadata.get_namespaces():
    logging.info('Switching namespace: \'%s\'', namespace)
    namespace_manager.set_namespace(namespace)
    update_per_namespace()

  return ('', 204)
