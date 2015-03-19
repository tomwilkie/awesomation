"""Philips hue proxy code."""

import abc
import logging
import sys
import threading


from pi import proxy


class ScanningProxy(proxy.Proxy):
  """A proxy object with a background scan thread."""
  __metaclass__ = abc.ABCMeta

  def __init__(self, refresh_period):
    self._refresh_period = refresh_period

    self._exiting = False
    self._scan_thread_condition = threading.Condition()
    self._scan_thread = threading.Thread(
        target=self._scan, name='%s thread' % self.__class__.__name__)
    self._scan_thread.daemon = True
    self._scan_thread.start()

  @proxy.command
  def scan(self):
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
        if self._exiting:
          break
        else:
          self._scan_thread_condition.wait(self._refresh_period)

    logging.info('Exited %s scan thread', self.__class__.__name__)

  @abc.abstractmethod
  def _scan_once(self):
    pass

  def stop(self):
    with self._scan_thread_condition:
      self._exiting = True
      self._scan_thread_condition.notify()

  def join(self):
    self._scan_thread.join()
