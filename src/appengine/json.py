"""JSON Encoder which encodes datetimes and ndb keys."""
import calendar
import datetime

from google.appengine.ext import ndb

import flask


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
