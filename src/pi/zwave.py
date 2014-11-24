"""ZWave device proxy code."""

import logging

import libopenzwave


class ZWave(object):
  """ZWave proxy object."""

  def __init__(self, device):
    self._device = device

    self._options = libopenzwave.PyOptions()
    self._options.create(
      libopenzwave.configPath(), '.', '')
    self._options.addOptionBool("ConsoleOutput", False)
    self._options.lock()

    self._manager = libopenzwave.PyManager()
    self._manager.create()
    self._manager.addWatcher(self._callback)
    self._manager.addDriver(self._device)

  def _callback(self, data):
    """Handle zwave events."""
    notification_type = data['notificationType']
    node_id = data['nodeId']

    if notification_type == 'Notification':
      logging.debug('ZWave callback - %s', data)
      return

    logging.info('ZWave callback - %s', data)

    if notification_type == 'NodeAdded':
      if node_id == 1:
        return

      self._manager.addAssociation(0, node_id, 1, 1)

  def handle_event(self, event):
    pass

  def stop(self):
    self._manager.removeWatcher(self._callback)
    self._manager.removeDriver(self._device)
