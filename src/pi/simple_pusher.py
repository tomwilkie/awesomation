"""A really dump pusher 'clone', for use in testing and running locally."""
import collections
import json
import logging
import SimpleHTTPServer
import SocketServer
import sys
import threading
import time

import SimpleWebSocketServer

HTTP_PORT = 8101
WEBSOCKET_PORT = 8102
SOCKETS = collections.defaultdict(list)


class SocketHandler(SimpleWebSocketServer.WebSocket):
  """Represents a websocket connection."""
  # pylint: disable=invalid-name

  def __init__(self, *args, **kwargs):
    super(SocketHandler, self).__init__(*args, **kwargs)
    self._channels = []

  def handleMessage(self):
    """Only message we get is a subscription."""
    if self.data is None:
      return

    try:
      # message should be a subscription, of form {channel: 'channel_name'}
      logging.info('\'%s\' received', self.data)
      data = json.loads(self.data.decode('utf-8'))
      self._channels.append(data['channel'])
      SOCKETS[data['channel']].append(self)
    except:
      logging.error('Error handling message:', exc_info=sys.exc_info())

  def handleConnected(self):
    logging.info('%s connected', self.address)

  def handleClose(self):
    logging.info('%s closed', self.address, exc_info=sys.exc_info())
    for channel in self._channels:
      SOCKETS[channel].remove(self)


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  """Represents a http requests."""
  # pylint: disable=invalid-name,too-many-public-methods

  def do_POST(self):
    """Send request body to /channel."""

    try:
      channel = self.path.split('/')[-1]
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)

      #logging.info('Sending \"%s\" to \"%s\"', post_body, channel)

      for socket in SOCKETS[channel]:
        socket.sendMessage(post_body)

      self.send_response(204, '')
    except:
      logging.error('Error sending message:', exc_info=sys.exc_info())


class SimplePusher(object):
  """A very simple websocket / push service."""
  def __init__(self):
    self._httpd = None
    self._httpd_thread = None
    self._websocket_server = None
    self._websocket_server_thread = None

  def start(self):
    """Start this."""
    logging.info('Starting local websocket server.')

    self._httpd = SocketServer.TCPServer(('', HTTP_PORT), ServerHandler)
    self._httpd_thread = threading.Thread(target=self._httpd.serve_forever)
    self._httpd_thread.start()

    self._websocket_server = SimpleWebSocketServer.SimpleWebSocketServer(
          '', WEBSOCKET_PORT, SocketHandler)
    self._websocket_server_thread = threading.Thread(
        target=self._websocket_server.serveforever)
    self._websocket_server_thread.start()

  def stop(self):
    """Stop this."""
    logging.info('Stopping local websocket server.')
    self._httpd.shutdown()
    self._httpd_thread.join()
    self._websocket_server.close()
    self._websocket_server_thread.join()


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  PUSHER = SimplePusher()
  PUSHER.start()

  try:
    while True:
      time.sleep(100)
  except:
    pass

  PUSHER.stop()

