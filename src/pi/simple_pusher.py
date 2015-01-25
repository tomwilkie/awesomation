"""A really dump pusher 'clone', for use in testing and running locally."""
import argparse
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
LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'


class SocketHandler(SimpleWebSocketServer.WebSocket):
  """Represents a websocket connection."""
  # pylint: disable=invalid-name
  def __init__(self, sockets, server, sock, address):
    super(SocketHandler, self).__init__(server, sock, address)
    self._sockets = sockets
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
      self._sockets[data['channel']].append(self)
    except:
      logging.error('Error handling message:', exc_info=sys.exc_info())

  def handleConnected(self):
    logging.info('%s connected', self.address)

  def handleClose(self):
    logging.info('%s closed', self.address, exc_info=sys.exc_info())
    for channel in self._channels:
      self._sockets[channel].remove(self)


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  """Represents a http requests."""
  # pylint: disable=invalid-name,too-many-public-methods
  def __init__(self, sockets, request, client_address, server):
    self._sockets = sockets
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(
        self, request, client_address, server)

  def do_POST(self):
    """Send request body to /channel."""
    try:
      channel = self.path.split('/')[-1]
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)

      #logging.info('Sending \"%s\" to \"%s\"', post_body, channel)

      for socket in self._sockets[channel]:
        socket.sendMessage(post_body)

      self.send_response(204, '')
    except:
      logging.error('Error sending message:', exc_info=sys.exc_info())


class SimplePusher(object):
  """A very simple websocket / push service."""
  def __init__(self, args):
    self._args = args
    self._sockets = collections.defaultdict(list)
    self._httpd = None
    self._httpd_thread = None
    self._websocket_server = None
    self._websocket_server_thread = None

  def _http_request_handler(self, request, client_address, server):
    return ServerHandler(self._sockets, request, client_address, server)

  def _websocket_request_handler(self, server, sock, addr):
    return SocketHandler(self._sockets, server, sock, addr)

  def start(self):
    """Start this."""
    logging.info('Starting local websocket server.')

    self._httpd = SocketServer.TCPServer(
        ('', self._args.http_port), self._http_request_handler)
    self._httpd_thread = threading.Thread(target=self._httpd.serve_forever)
    self._httpd_thread.start()

    self._websocket_server = SimpleWebSocketServer.SimpleWebSocketServer(
        '', self._args.websocket_port, self._websocket_request_handler)
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


def main():
  logging.basicConfig(format=LOGFMT, level=logging.DEBUG)

  parser = argparse.ArgumentParser()
  parser.add_argument('--http_port',
                      default=HTTP_PORT)
  parser.add_argument('--websocket_port',
                      default=WEBSOCKET_PORT)
  args = parser.parse_args()

  pusher = SimplePusher(args)
  pusher.start()

  try:
    while True:
      time.sleep(100)
  except:
    pass

  pusher.stop()


if __name__ == '__main__':
  main()

