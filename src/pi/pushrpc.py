import json
import logging
import Queue

from common import creds
from pusherclient import Pusher


class PushRPC(object):
  
  def __init__(self):
    self._queue = Queue.Queue()
    self._pusher = Pusher(creds.pusher_key)
    self._pusher.connection.bind('pusher:connection_established',
      self._ConnectHandler)
    self._pusher.connect()

  def _ConnectHandler(self, data):
    channel = self._pusher.subscribe('test')
    channel.bind('event', self._Callback)
        
  def _Callback(self, data):
    try:
      data = json.loads(data)            
    except Exception, e:
      logging.error('Error parsing message', e)
      return
    self._queue.put(data)
    
  def Events(self):
    while True:
      yield self._queue.get(block=True)

