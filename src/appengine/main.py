"""Main module for appengine app."""
import calendar
import datetime
import logging
import os
import sys

from google.appengine.ext import ndb

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../third_party'))

import flask

from appengine import account, device, driver, history
from appengine import pushrpc, room, tasks, user

# This has the side effect of registering devices
# pylint: disable=unused-wildcard-import,wildcard-import
from appengine.devices import *
from appengine.devices.zwave_drivers import *


# Configure logging
logging.getLogger('boto').setLevel(logging.INFO)


def static_dir():
  return os.path.normpath(os.path.join(os.path.dirname(__file__), '../static'))


class Encoder(flask.json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      if obj.utcoffset() is not None:
        obj = obj - obj.utcoffset()

      millis = int(
          calendar.timegm(obj.timetuple()) * 1000 +
          obj.microsecond / 1000)

      return millis

    elif isinstance(obj, ndb.Key):
      return obj.string_id()

    else:
      return flask.json.JSONEncoder.default(self, obj)


# pylint: disable=invalid-name
app = flask.Flask('awesomation', static_folder=static_dir())
app.debug = True
app.json_encoder = Encoder

# These are not namespaced
app.register_blueprint(user.blueprint, url_prefix='/api/user')
app.register_blueprint(pushrpc.blueprint, url_prefix='/api/proxy')
app.register_blueprint(tasks.blueprint, url_prefix='/tasks')

# There are all namespaced
app.register_blueprint(account.blueprint, url_prefix='/api/account')
app.register_blueprint(device.blueprint, url_prefix='/api/device')
app.register_blueprint(driver.blueprint, url_prefix='/api/driver')
app.register_blueprint(room.blueprint, url_prefix='/api/room')


@app.route('/')
def root():
  return flask.send_from_directory(static_dir(), 'index.html')


@app.errorhandler(400)
def custom400(error):
  response = flask.jsonify({'message': error.description})
  return response, 400


@app.after_request
def after_request(response):
  pushrpc.push_batch()
  user.push_events()
  history.store_batch()
  return response

