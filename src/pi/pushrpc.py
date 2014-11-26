"""Pusher intergration for messages from the cloud."""

import httplib
import json
import logging
import Queue
import sys
import threading

from common import creds
from pusherclient import Pusher


def _post_events_once(events):
  """Send list of events to server."""
  logging.info('Posting %d events to server', len(events))

  body = json.dumps(events)
  headers = {'Content-type': 'application/json',
             'Accept': 'text/plain'}
  conn = httplib.HTTPSConnection('%s.appspot.com' % creds.appengine_app_id)
  conn.request('POST', '/api/device/events', body, headers)
  response = conn.getresponse()
  if not (200 <= response.status < 300):
    logging.error('Response %d from server - \'%s\'',
                  response.status, response.reason)
  conn.close()


class PushRPC(object):
  """Wrapper for pusher integration."""

  def __init__(self, callback):
    self._exiting = False

    self._events = Queue.Queue()
    self._events_thread = threading.Thread(target=self._post_events_loop)
    self._events_thread.daemon = True
    self._events_thread.start()

    self._callback = callback

    self._pusher = Pusher(creds.pusher_key)
    self._pusher.connection.bind(
        'pusher:connection_established',
        self._connect_handler)
    self._pusher.connect()

  def _connect_handler(self, _):
    channel = self._pusher.subscribe('test')
    channel.bind('event', self._callback_handler)

  def _callback_handler(self, data):
    """Callback for when messages are recieved from pusher."""
    try:
      data = json.loads(data)
    except ValueError:
      logging.error('Error parsing message', exc_info=sys.exc_info())
      return

    # pylint: disable=broad-except
    try:
      self._callback(data)
    except Exception:
      logging.error('Error running push callback', exc_info=sys.exc_info())

  def send_event(self, event):
    self._events.put(event)

  def _get_batch_of_events(self):
    """Retrieve as many events from queue as possible without blocking."""
    events = []
    while True:
      try:
        # First time round we should wait (when list is empty)
        event = self._events.get(len(events) == 0)

        # To break out of this thread, we inject a None event in stop()
        if event is None:
          return None

        events.append(event)
      except Queue.Empty:
        break

    assert events
    return events

  def _post_events_loop(self):
    """Send batched of events to server in a loop."""
    logging.info('Starting events thread.')
    while not self._exiting:
      events = self._get_batch_of_events()
      if events is None:
        break

      # pylint: disable=broad-except
      try:
        _post_events_once(events)
      except Exception:
        logging.error('Exception sending events to server',
                      exc_info=sys.exc_info())
    logging.info('Exiting events thread.')

  def stop(self):
    """Stop various threads and connections."""
    self._exiting = True
    self._events.put(None)
    self._events_thread.join()

    self._pusher.disconnect()
