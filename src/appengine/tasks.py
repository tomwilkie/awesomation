"""Regular update task."""

import logging

from google.appengine.ext.ndb import metadata
from google.appengine.api import namespace_manager

import flask

from appengine.devices import nest


# pylint: disable=invalid-name
blueprint = flask.Blueprint('tasks', __name__)


def update_per_namespace():
  accounts = nest.NestAccount.query().iter()
  for account in accounts:
    account.refresh_devices()
    account.put()


@blueprint.route('/update', methods=['GET'])
def update():
  logging.info('Update task.')

  for namespace in metadata.get_namespaces():
    logging.info("namespace: '%s'", namespace)
    namespace_manager.set_namespace(namespace)
    update_per_namespace()

  return ('', 204)
