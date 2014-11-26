"""ZWave device proxy code."""

import logging
import sys

import libopenzwave


class ZWave(object):
  """ZWave proxy object."""

  def __init__(self, device, callback):
    self._device = device
    self._callback = callback

    self._options = libopenzwave.PyOptions()
    self._options.create(
        libopenzwave.configPath(), '.', '')
    self._options.addOptionBool("ConsoleOutput", False)
    self._options.lock()

    self._manager = libopenzwave.PyManager()
    self._manager.create()
    self._manager.addWatcher(self._zwave_callback)
    self._manager.addDriver(self._device)

  def _zwave_callback(self, data):
    # pylint: disable=broad-except
    try:
      self._zwave_callback_internal(data)
    except Exception:
      logging.error('Exception during zwave event', exc_info=sys.exc_info())

  def _zwave_callback_internal(self, data):
    """Handle zwave events."""
    notification_type = data['notificationType']
    home_id = data['homeId']
    node_id = data['nodeId']

    logging.info('ZWave callback - %d %s', node_id, notification_type)

    if node_id in {1, 255}:
      return

    if notification_type == 'NodeAdded':
      self._manager.addAssociation(home_id, node_id, 1, 1)
      self._manager.refreshNodeInfo(home_id, node_id)
      self._manager.requestNodeState(home_id, node_id)
      self._manager.requestNodeDynamic(home_id, node_id)

    elif notification_type in {'ValueAdded', 'ValueChanged', 'NodeNaming'}:
      #logging.info('%s', data)
      self._callback('zwave', 'zwave-%d' % node_id, data)

  def handle_event(self, event):
    pass

  def stop(self):
    self._manager.removeWatcher(self._callback)
    self._manager.removeDriver(self._device)
