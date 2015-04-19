"""Handle user related queries."""
import base64
import collections
import logging
import re
import zlib

import flask
import pusher

from appengine import pusher_client
from common import public_creds, utils
from pi import simple_pusher

batcher = common.Batcher(push_events)


def send_event(**kwargs):
  """Send an event to listening UIs."""
  batcher.queue(kwargs)


def push_events(events):
  """Push all the events that have been caused by this request."""
  compressed_events = []
  for event in events:
    # The UI can deal with compressed and uncompressed events.
    # Lets compress the event, base64 encode it, and it thats
    # shorter send that.  Otherwise send the original event.
    encoded_event = flask.json.dumps(event)
    compressed_event = zlib.compress(encoded_event)
    compressed_event = base64.b64encode(compressed_event)
    if len(encoded_event) > len(compressed_event):
      event = {'c': compressed_event}
    compressed_events.append(event)

  pusher_shim = pusher_client.get_client(encoder=flask.json.JSONEncoder)
  channel_id = 'events'

  for batch in utils.limit_json_batch(events, max_size=8000):
    logging.info('Sending %d events to user on channel %s',
                 len(batch), channel_id)
    pusher_shim.push(channel_id, batch)
