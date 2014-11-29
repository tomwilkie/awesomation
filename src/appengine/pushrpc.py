"""Code to push events to users."""

import logging

import pusher

from common import creds


def send_event(user_id, event):
  """Post events back to the pi."""
  logging.info('%s <- %s', user_id, event)

  pusher_client = pusher.Pusher(
      app_id=creds.pusher_app_id,
      key=creds.pusher_key, secret=creds.pusher_secret)
  pusher_client['test'].trigger('event', event)
