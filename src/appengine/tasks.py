"""Regular update task."""

import logging

import flask


# pylint: disable=invalid-name
blueprint = flask.Blueprint('tasks', __name__)


@blueprint.route('/update', methods=['GET'])
def update():
  logging.info('Update task.')
  return ('', 204)
