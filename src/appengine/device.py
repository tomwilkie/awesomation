"""Factory for creating devices."""
import logging

from google.appengine.ext import db

import flask

from appengine import model, hue, rfswitch, user, zwave

# pylint: disable=invalid-name
blueprint = flask.Blueprint('device', __name__)


def create_device(device_id, device_type, user_id):
  """Factory for creating new devices."""
  if device_type == 'zwave':
    return zwave.ZWaveDevice(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'rfswitch':
    return rfswitch.RFSwitch(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'hue_bridge':
    return hue.HueBridge(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  elif device_type == 'hue_light':
    return hue.HueLight(
        id='%s-%s' % (user_id, device_id), owner=user_id)
  else:
    assert False


@blueprint.route('/events', methods=['POST'])
def handle_events():
  """Handle events from devices."""
  user_id = '102063417381751091397'
  events = flask.request.get_json()
  logging.info('Processing %d events', len(events))

  device_cache = {}

  for event in events:
    device_type = event['device_type']
    device_id = event['device_id']
    event_body = event['event']

    if device_id in device_cache:
      device = device_cache[device_id]
    else:
      device = model.Device.get_by_id('%s-%s' % (user_id, device_id))
      if not device:
        device = create_device(device_id, device_type, user_id)
      device_cache[device_id] = device

    device.handle_event(event_body)

  for device in device_cache.itervalues():
    device.put()

  return ('', 204)


@blueprint.route('/', methods=['GET'])
def list_devices():
  """Return json list of devices."""
  user_id = user.get_user()
  device_list = model.Device.query(model.Device.owner == user_id).iter()
  if device_list is None:
    device_list = []

  device_list = [device.to_dict() for device in device_list]
  return flask.jsonify(devices=device_list)


@blueprint.route('/<device_id>', methods=['POST'])
def create_update_device(device_id):
  """Using json body to create or update a device."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  device = model.Device.get_by_id('%s-%s' % (user_id, device_id))

  if not device:
    device_type = body.pop('type', None)
    if device_type is None:
      flask.abort(400, '\'type\' field expected in body.')

    device = create_device(
        device_id, device_type, user_id)

  elif device.owner != user_id:
    flask.abort(403)

  # Update the object; abort with 400 on unknown field
  try:
    device.populate(**body)
  except AttributeError, err:
    flask.abort(400)

  # Put the object - BadValueError if there are uninitalised required fields
  try:
    device.put()
  except db.BadValueError, err:
    flask.abort(400)

  return flask.jsonify(**device.to_dict())


@blueprint.route('/<device_id>', methods=['GET'])
def get_device(device_id):
  """Return json repr of given device."""
  user_id = user.get_user()
  device = model.Device.get_by_id('%s-%s' % (user_id, device_id))

  if not device:
    flask.abort(404)
  elif device.owner != user_id:
    flask.abort(403)

  return flask.jsonify(**device.to_dict())


@blueprint.route('/<device_id>/command', methods=['POST'])
def device_command(device_id):
  """Using json body to create or update a device."""
  user_id = user.get_user()
  body = flask.request.get_json()
  if body is None:
    flask.abort(400, 'JSON body and mime type required.')

  device = model.Device.get_by_id('%s-%s' % (user_id, device_id))

  if not device:
    flask.abort(404)
  elif device.owner != user_id:
    flask.abort(403)

  device.handle_command(body)

  return ('', 204)
