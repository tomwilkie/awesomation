import argparse
import logging
import sys
import threading

import store
from pi import control
from pi import simple_pusher
import appengine.main

LOGFMT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'
PIDFILE = '/var/run/control.pid'
LOGFILE = '/var/log/control.log'
STATEDIR = '.'

def main():
  """Main function."""
  # Setup logging
  logging.basicConfig(format=LOGFMT, level=logging.INFO)
  logging.getLogger(
    'requests.packages.urllib3.connectionpool').setLevel(logging.ERROR)
  logging.getLogger('soco.services').setLevel(logging.ERROR)

  # Arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--daemonize', dest='daemonize', action='store_true')
  parser.add_argument('--nodaemonize', dest='daemonize', action='store_false')
  parser.set_defaults(daemonize=True)

  parser.add_argument('--local', dest='local', action='store_true')
  parser.add_argument('--nolocal', dest='local', action='store_false')
  parser.set_defaults(daemonize=False)

  parser.add_argument('--http-port', default=8080)

  parser.add_argument('--zwave_device',
                      default='/dev/ttyUSB0')
  parser.add_argument('--rfswtich_pin',
                      default=3)
  parser.add_argument('--hue_scan_interval_secs',
                      default=5*60)
  parser.add_argument('--network_scan_interval_secs',
                      default=10)
  parser.add_argument('--network_scan_timeout_secs',
                      default=5*60)
  args = parser.parse_args()

  # read the store from disk
  s = store.Store(STATEDIR)
  s.load()
  appengine.model.Base.set_store(s)

  # start the pi code
  c = control.Control(args, appengine.device.handle_event)
  appengine.pushrpc.event_callback = c._push_event_callback
  c.start()

  # start the websocker server
  #pusher = simple_pusher.SimplePusher(args)
  #pusher.start()

  # start the app
  appengine.main.app.run(port=args.http_port)

  logging.info("App exiting...")
  c.stop()

if __name__ == '__main__':
  main()
