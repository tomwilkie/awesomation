"""ZWave device proxy code."""

import logging
import sys

import libopenzwave


CONFIG = '/usr/local/etc/openzwave'

class ZWave(object):
  """ZWave proxy object."""

  def __init__(self, device, callback):
    self._device = device
    self._callback = callback

    self._options = libopenzwave.PyOptions()
    self._options.create(CONFIG, '/home/pi/openzwave', '')
    self._options.addOptionBool('ConsoleOutput', False)
    self._options.addOptionInt('SaveLogLevel', 7) # INFO
    self._options.addOptionInt('QueueLogLevel', 7) # INFO
    self._options.lock()

    self._manager = libopenzwave.PyManager()
    self._manager.create()
    self._manager.addWatcher(self._zwave_callback)
    self._manager.addDriver(self._device)

    self._home_id = None

  def _zwave_callback(self, data):
    # pylint: disable=broad-except
    try:
      self._zwave_callback_internal(data)
    except Exception:
      logging.error('Exception during zwave event', exc_info=sys.exc_info())

  def _zwave_callback_internal(self, data):
    """Handle zwave events."""
    notification_type = data['notificationType']
    self._home_id = data['homeId']
    node_id = data['nodeId']

    logging.info('ZWave callback - %d %s', node_id, notification_type)

    if node_id in {1, 255}:
      return

    if notification_type == 'NodeAdded':
      self._manager.addAssociation(self._home_id, node_id, 1, 1)
      self._manager.refreshNodeInfo(self._home_id, node_id)
      self._manager.requestNodeState(self._home_id, node_id)
      self._manager.requestNodeDynamic(self._home_id, node_id)

    elif notification_type in {'ValueAdded', 'ValueChanged', 'NodeNaming'}:
      #logging.info('%s', data)
      self._callback('zwave', 'zwave-%d' % node_id, data)

    else: #if notification_type in {'NodeEvent'}:
      logging.info(data)

  def handle_events(self, messages):
    for message in messages:
      command = message.pop('command')
      if command == 'heal':
        self._manager.softResetController(self._home_id)
        self._manager.healNetwork(self._home_id)

  def stop(self):
    if self._home_id is not None:
      self._manager.writeConfig(self._home_id)
    self._manager.removeWatcher(self._callback)
    self._manager.removeDriver(self._device)
