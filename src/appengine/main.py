import json
import logging
import os
import random
import string
import sys

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../third_party'))

import flask
from flask import request

import accounts
import model
import pusher
from common import creds

def StaticDir():
  return os.path.normpath(os.path.join(os.path.dirname(__file__), '../static'))

app = flask.Flask('domics', static_folder=StaticDir())
app.debug = True

@app.route('/')
def Root():
    return flask.send_from_directory(StaticDir(), 'index.html')


@app.before_request
def BeforeRequest():
  user = users.get_current_user()
  if not user and request.endpoint not in {'/'}:        
    return flaskredirect(users.create_login_url(request.endpoint))
  logging.info(user) 
  person = model.Person.get_or_insert(key_name=user.user_id())


def GetUser():
  user = users.get_current_user()
  assert user is not None
  return model.Person.get_or_insert(key_name=user.user_id())


@app.route('/api/user', methods=['GET'])
def GetUserRequest():
  user = GetUser()
  return flask.jsonify(id=user.key().id_or_name(), **db.to_dict(user))


@app.route('/api/channel')
def post(chan_name):
  event = json.loads(self.request.body)
  print event
  p = pusher.Pusher(app_id=creds.pusher_app_id, 
    key=creds.pusher_key, secret=creds.pusher_secret)
  p[chan_name].trigger('event', event)


@app.route('/api/device/<int:device_id>', methods=['POST'])
def CreateUpdateDevice(device_id):
  body = json.loads(flask.request.data)
  device = model.Device.get_by_id(device_id)
  if not device:
    device = Devices.CreateDevice(body)
  else:
    device.update(body)
  device.put()


@app.route('/api/device/<int:device_id>', methods=['GET'])
def GetDevice(device_id):
  device = model.Device.get_by_id(device_id)
  if not device:
      flask.abort(404)
  return flask.jsonify(**db.to_dict(device))


@app.route('/api/device/<int:device_id>/event')
def DeviceEvent(device_id):
  device = model.Device.get_by_id(device_id)
  if not device:
    flask.abort(404)
  event = json.loads(flask.request.data)
  device.Event(event)

