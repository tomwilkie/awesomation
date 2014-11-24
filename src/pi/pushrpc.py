"""Pusher intergration for messages from the cloud."""

import json
import logging
import Queue
import sys

from common import creds
from pusherclient import Pusher


class PushRPC(object):
  """Wrapper for pusher integration."""

  def __init__(self):
    self._queue = Queue.Queue()
    self._pusher = Pusher(creds.pusher_key)
    self._pusher.connection.bind('pusher:connection_established',
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
    self._queue.put(data)

  def events(self):
    while True:
      # if we specify a timeout, queues become keyboard interruptable
      try:
        yield self._queue.get(block=True, timeout=1000)
      except Queue.Empty:
        pass

