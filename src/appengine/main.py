"""Main module for appengine app."""

import calendar
import datetime
import os
import sys

from google.appengine.api import namespace_manager, users
from google.appengine.ext import ndb

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../third_party'))

import flask

from appengine import device, driver, pushrpc, room, tasks, user
# This has the side effect of registering devices
# pylint: disable=unused-wildcard-import,wildcard-import
from appengine.devices import *


def static_dir():
  return os.path.normpath(os.path.join(os.path.dirname(__file__), '../static'))


class CustomJSONEncoder(flask.json.JSONEncoder):

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
app = flask.Flask('domics', static_folder=static_dir())
app.debug = True
app.json_encoder = CustomJSONEncoder
app.register_blueprint(user.blueprint, url_prefix='/api/user')
app.register_blueprint(device.blueprint, url_prefix='/api/device')
app.register_blueprint(driver.blueprint, url_prefix='/api/driver')
app.register_blueprint(room.blueprint, url_prefix='/api/room')
app.register_blueprint(pushrpc.blueprint, url_prefix='/api/proxy')
app.register_blueprint(tasks.blueprint, url_prefix='/tasks')


@app.route('/')
def root():
  return flask.send_from_directory(static_dir(), 'index.html')


@app.before_request
def before_request():
  """Ensure user is authenticated."""

  # Proxies use basic authentication, and are only allowed a few endpoints
  if flask.request.headers.get('awesomation-proxy', None) == 'true':
    proxy = pushrpc.authenticate()
    if proxy is None:
      flask.abort(401)

    # we don't set the namespace to the owner,
    # as we need to authenticate proxy requests
    # before owner is set (ie proxies are unclaimed)
    # namespace_manager.set_namespace(proxy.owner)
    return

  # Cron jobs are authenticated as a special case
  if flask.request.endpoint in {'tasks.update'}:
    if flask.request.headers.get('X-AppEngine-Cron', None) != 'true':
      flask.abort(401)
    return

  # Otherwise, we just use good-ole google authentication
  user_object = users.get_current_user()
  if not user_object:
    return flask.redirect(users.create_login_url(flask.request.url))

  namespace_manager.set_namespace(user_object.user_id())


@app.after_request
def after_request(response):
  pushrpc.push_batch()
  return response
