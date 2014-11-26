"""Main module for appengine app."""

import json
import logging
import os
import sys

from google.appengine.api import users
from google.appengine.ext import db

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../third_party'))

import flask
import pusher

from appengine import model, devices
from common import creds


def static_dir():
  return os.path.normpath(os.path.join(os.path.dirname(__file__), '../static'))

# pylint: disable=invalid-name
app = flask.Flask('domics', static_folder=static_dir())
app.debug = True


@app.route('/')
def root():
  return flask.send_from_directory(static_dir(), 'index.html')


@app.before_request
def before_request():
  """Ensure user is authenticated."""
  if flask.request.endpoint in {'root', 'device_events'}:
    return

  user = users.get_current_user()
  if not user:
    return flask.redirect(users.create_login_url(flask.request.endpoint))
  logging.info(user)
  model.Person.get_or_insert(key_name=user.user_id())


def get_user():
  user = users.get_current_user()
  assert user is not None
  return model.Person.get_or_insert(key_name=user.user_id())


@app.route('/api/user', methods=['GET'])
def get_user_request():
  user = get_user()
  return flask.jsonify(id=user.key().id_or_name(), **db.to_dict(user))


@app.route('/api/channel')
def post(chan_name):
  """Post events back to the pi."""
  event = json.loads(flask.request.body)
  p = pusher.Pusher(app_id=creds.pusher_app_id,
    key=creds.pusher_key, secret=creds.pusher_secret)
  p[chan_name].trigger('event', event)


@app.route('/api/device/events', methods=['POST'])
def device_events():
  """Handle events from devices."""

  events = flask.request.get_json()
  logging.info(events)

  for event in events:
    device_type = event['device_type']
    device_id = event['device_id']
    event_body = event['event']

    device = model.Device.get_by_key_name(device_id)
    if not device:
      device = devices.create_device(device_id, device_type)

    device.event(event_body)
    device.put()

  return ('', 204)


@app.route('/api/device', methods=['GET'])
def list_devices():
  """Return json list of devices."""
  device_list = model.Device.all().get()
  if device_list is None:
    device_list = []
  device_list = [db.to_dict(device) for device in device_list]
  return flask.jsonify(devices=devices)


@app.route('/api/device/<int:device_id>', methods=['POST'])
def create_update_device(device_id):
  """Using json body to create or update a device."""
  body = flask.request.get_json()
  device = model.Device.get_by_key_name(device_id)
  if not device:
    device_type = body['type']
    device = devices.create_device(
        device_id, device_type=device_type, params=body)
  else:
    device.update(body)
  device.put()


@app.route('/api/device/<int:device_id>', methods=['GET'])
def get_device(device_id):
  device = model.Device.get_by_key_name(device_id)
  if not device:
    flask.abort(404)
  return flask.jsonify(**db.to_dict(device))


