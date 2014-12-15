"""Philips hue proxy code."""

import logging
import sys
import threading


class ScanningProxy(object):
  """A proxy object with a background scan thread."""

  def __init__(self, refresh_period):
    self._refresh_period = refresh_period

    self._exiting = False
    self._scan_thread_condition = threading.Condition()
    self._scan_thread = threading.Thread(target=self._scan)
    self._scan_thread.daemon = True
    self._scan_thread.start()

  def _trigger_scan(self):
    with self._scan_thread_condition:
      self._scan_thread_condition.notify()

  def _scan(self):
    """Loop thread for scanning."""
    while not self._exiting:
      # We always do a scan on start up.
      try:
        self._scan_once()
      except:
        logging.error('Error during %s scan', self.__class__.__name__,
                      exc_info=sys.exc_info())

      with self._scan_thread_condition:
        self._scan_thread_condition.wait(self._refresh_period)
        if self._exiting:
          break
    logging.info('Exiting %s scan thread', self.__class__.__name__)

  def _bridge_scan_once(self):
    pass

  def handle_events(self, messages):
    """Handle hue events - turn it on or off."""
    for message in messages:
      command = message.pop('command')

      if command == 'scan':
        self._trigger_bridge_scan()
      else:
        logging.info('Unhandled message type \'%s\'', command)

  def stop(self):
    self._exiting = True
    self._trigger_scan()
    self._scan_thread.join()
