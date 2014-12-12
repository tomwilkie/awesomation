"""Code to push events to users."""

import logging

import flask
import pusher

from common import creds


def push_batch():
  """Push all the events that have been caused by this request."""
  batch = flask.g.get('events', None)
  if batch is None:
    return

  logging.info('Pushing %d events', len(batch))
  pusher_client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=creds.pusher_key, secret=creds.pusher_secret)
  pusher_client['test'].trigger('events', batch)


def send_event(user_id, event):
  """Post events back to the pi."""
  logging.info('%s <- %s', user_id, event)
  batch = flask.g.get('events', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'events', batch)
  batch.append(event)

