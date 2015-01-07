"""A generic rest serving layer for NDB models."""
import logging
import sys

from google.appengine.ext import db

import flask
import flask.views

from appengine import user


def command(func):
  """Command decorator - automatically dispatches methods."""
  setattr(func, 'is_command', True)
  return func


class ClassView(flask.views.MethodView):
  """Implements create, retrieve, update and removed endpoints for models."""

  def __init__(self, classname, cls, create_callback):
    super(ClassView, self).__init__()
    self._classname = classname
    self._cls = cls
    self._create_callback = create_callback

  def get(self, object_id):
    """List objects or just return a single object."""
    if object_id is None:
      # Return json list of objects.
      object_list = self._cls.query().iter()
      if object_list is None:
        object_list = []

      object_list = [obj.to_dict() for obj in object_list]
      return flask.jsonify(objects=object_list)

    else:
      # Return json repr of given object
      user_id = user.get_user()
      obj = self._cls.get_by_id(object_id)

      if not obj:
        flask.abort(404)
      elif obj.owner != user_id:
        flask.abort(403)

      return flask.jsonify(**obj.to_dict())

  def post(self, object_id):
    """Using json body to create or update a object."""
    user_id = user.get_user()
    body = flask.request.get_json()
    if body is None:
      flask.abort(400, 'JSON body and mime type required.')
    logging.info("Creating (or updating) object - %s", body)

    obj = self._cls.get_by_id(object_id)

    if not obj and self._create_callback is None:
      flask.abort(403)
    elif not obj:
      obj = self._create_callback(object_id, user_id, body)

    elif obj.owner != user_id:
      flask.abort(403)

    # Update the object; abort with 400 on unknown field
    try:
      obj.populate(**body)
    except AttributeError:
      logging.error('Exception populating object', exc_info=sys.exc_info())
      flask.abort(400)

    # Put the object - BadValueError if there are uninitalised required fields
    try:
      obj.put()
    except db.BadValueError:
      logging.error('Exception saving object', exc_info=sys.exc_info())
      flask.abort(400)

    values = obj.to_dict()
    user.send_event(cls=self._classname, id=object_id,
                    event='update', obj=values)

    return flask.jsonify(**values)

  def delete(self, object_id):
    """Delete an object."""
    user_id = user.get_user()
    obj = self._cls.get_by_id(object_id)

    if not obj:
      flask.abort(404)
    elif obj.owner != user_id:
      flask.abort(403)

    obj.key.delete()
    user.send_event(cls=self._classname, id=object_id, event='delete')
    return ('', 204)


class CommandView(flask.views.MethodView):
  """Implements /command endpoints for models."""

  def __init__(self, classname, cls):
    super(CommandView, self).__init__()
    self._classname = classname
    self._cls = cls

  def post(self, object_id):
    """Run a command on a object."""
    user_id = user.get_user()
    body = flask.request.get_json()
    if body is None:
      flask.abort(400, 'JSON body and mime type required.')

    logging.info(body)
    obj = self._cls.get_by_id(object_id)

    if not obj:
      flask.abort(404)
    elif obj.owner != user_id:
      flask.abort(403)

    func_name = body.pop('command', None)
    func = getattr(obj, func_name, None)
    if func is None or not func.is_command:
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)

    result = func(**body)

    obj.put()
    user.send_event(cls=self._classname, id=object_id,
                    event='update', obj=obj.to_dict())

    return flask.jsonify(result=result)


def register_class(blueprint, cls, create_callback):
  """Register a ndb model for rest endpoints."""
  class_view_func = ClassView.as_view('%s_crud' % cls.__name__,
                                      blueprint.name, cls, create_callback)
  blueprint.add_url_rule('/', defaults={'object_id': None},
                         view_func=class_view_func, methods=['GET',])
  blueprint.add_url_rule('/<object_id>', view_func=class_view_func,
                         methods=['GET', 'POST', 'DELETE'])

  command_view_func = CommandView.as_view('%s_command' % cls.__name__,
                                          blueprint.name, cls)
  blueprint.add_url_rule('/<object_id>/command', methods=['POST'],
                         view_func=command_view_func)
