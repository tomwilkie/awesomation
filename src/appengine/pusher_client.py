"""Abstraction between production pusher and local test."""
import json
import logging
import os

from google.appengine.api import urlfetch

import pusher

from common import public_creds
from pi import simple_pusher


class PusherWrapper(object):
  """Wraps the pusher client library, """
  def __init__(self, **kwargs):
    # Hack, but some people won't have this (when running locally)
    from common import creds
    self._pusher_client = pusher.Pusher(
        app_id=creds.PUSHER_APP_ID,
        key=public_creds.pusher_key, secret=creds.PUSHER_SECRET,
        **kwargs)

  def push(self, channel_id, batch):
    self._pusher_client[channel_id].trigger('events', batch)


class SimplePusherWrapper(object):
  def __init__(self, encoder=None):
    self._encoder = encoder if encoder is not None else json.JSONEncoder

  def push(self, channel_id, batch):
    url = 'http://localhost:%d/%s' % (simple_pusher.HTTP_PORT, channel_id)
    payload = self._encoder().encode(batch)
    urlfetch.fetch(url=url, payload=payload, method=urlfetch.POST)


def should_use_local():
  return os.environ['APPLICATION_ID'].startswith('dev')


def get_client(**kwargs):
  # If we are running in local mode,
  # we want to push events to our local,
  # hacked up server.
  if should_use_local():
    logging.info('Using local simple pusher.')
    return SimplePusherWrapper(**kwargs)
  else:
    return PusherWrapper(**kwargs)
