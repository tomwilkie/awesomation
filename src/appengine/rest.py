"""A generic rest serving layer for NDB models."""
import logging
import sys

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
    default_user_authentication()

    if object_id is None:
      # Return json list of objects.
      object_list = self._cls.query().iter()
      if object_list is None:
        object_list = []

      object_list = [obj.to_dict() for obj in object_list]
      return flask.jsonify(objects=object_list)

    else:
      # Return json repr of given object
      obj = self._cls.get_by_id(object_id)

      if not obj:
        flask.abort(404)

      return flask.jsonify(**obj.to_dict())

  def post(self, object_id):
    """Using json body to create or update a object."""
    default_user_authentication()

    body = flask.request.get_json()
    if body is None:
      flask.abort(400, 'JSON body and mime type required.')
    logging.info("Creating (or updating) object - %s", body)

    obj = self._cls.get_by_id(object_id)

    if not obj and self._create_callback is None:
      flask.abort(403)
    elif not obj:
      obj = self._create_callback(object_id, body)

    # Update the object; abort with 400 on unknown field
    try:
      obj.populate(**body)
    except AttributeError:
      logging.error('Exception populating object', exc_info=sys.exc_info())
      flask.abort(400)

    obj.sync()

    # Put the object - BadValueError if there are uninitalised required fields
    try:
      obj.put()
    except db.BadValueError:
      logging.error('Exception saving object', exc_info=sys.exc_info())
      flask.abort(400)

    values = obj.to_dict()
    return flask.jsonify(**values)

  def delete(self, object_id):
    """Delete an object."""
    default_user_authentication()

    obj = self._cls.get_by_id(object_id)

    if not obj:
      flask.abort(404)

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
    default_user_authentication()

    body = flask.request.get_json()
    if body is None:
      flask.abort(400, 'JSON body and mime type required.')

    logging.info(body)
    obj = self._cls.get_by_id(object_id)

    if not obj:
      flask.abort(404)

    func_name = body.pop('command', None)
    func = getattr(obj, func_name, None)
    if func is None or not getattr(func, 'is_command', False):
      logging.error('Command %s does not exist or is not a command',
                    func_name)
      flask.abort(400)

    result = func(**body)
    obj.put()
    return flask.jsonify(result=result)


class HistoryView(flask.views.MethodView):
  """Implements /history endpoints for models."""

  def __init__(self, classname, cls):
    super(HistoryView, self).__init__()
    self._classname = classname
    self._cls = cls

  def post(self, object_id):
    """Fetch the history for an object."""
    default_user_authentication()

    body = flask.request.get_json()
    if body is None:
      flask.abort(400, 'JSON body and mime type required.')

    start_time = body.pop('start_time', None)
    end_time = body.pop('end_time', None)
    if start_time is None or end_time is None:
      flask.abort(400, 'start_time and end_time expected.')

    obj = self._cls.get_by_id(object_id)
    if not obj:
      flask.abort(404)

    result = obj.get_history(start=start_time, end=end_time)
    result = list(result)
    return flask.jsonify(result=result)


def default_user_authentication():
  """Ensure user is authenticated, and switch to
     appropriate building namespace."""

  user_object = user.get_user_object()
  if not user_object:
    return flask.abort(401)

  # Need to pick a building for this user request
  person = user.get_person()
  buildings = list(person.buildings)
  assert len(buildings) > 0
  buildings.sort()

  if 'building-id' in flask.request.headers:
    building_id = flask.request.headers['building-id']
    if building_id not in buildings:
      flask.abort(401)
  else:
    building_id = buildings[0]

  namespace_manager.set_namespace(building_id)


def register_class(blueprint, cls, create_callback):
  """Register a ndb model for rest endpoints."""

  # register some handlers
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

  history_view_func = HistoryView.as_view('%s_history' % cls.__name__,
                                          blueprint.name, cls)
  blueprint.add_url_rule('/<object_id>/history', methods=['POST'],
                         view_func=history_view_func)
