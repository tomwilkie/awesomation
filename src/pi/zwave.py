"""ZWave device proxy code."""

import logging
import sys

import libopenzwave

from pi import proxy


CONFIG = '/usr/local/etc/openzwave'


class ZWave(proxy.Proxy):
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
    self._node_ids = set()

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

    if notification_type == 'AwakeNodesQueried':
      for node_id in self._node_ids:
        node_info = {'notificationType': 'NodeInfoUpdate'}
        node_info['basic'] = self._manager.getNodeBasic(
            self._home_id, node_id)
        node_info['generic'] = self._manager.getNodeGeneric(
            self._home_id, node_id)
        node_info['specific'] = self._manager.getNodeSpecific(
            self._home_id, node_id)
        node_info['node_type'] = self._manager.getNodeType(
            self._home_id, node_id)
        node_info['node_name'] = self._manager.getNodeName(
            self._home_id, node_id)
        node_info['manufacturer_name'] = self._manager.getNodeManufacturerName(
            self._home_id, node_id)
        node_info['manufacturer_id'] = self._manager.getNodeManufacturerId(
            self._home_id, node_id)
        node_info['product_name'] = self._manager.getNodeProductName(
            self._home_id, node_id)
        node_info['product_type'] = self._manager.getNodeProductType(
            self._home_id, node_id)
        node_info['product_id'] = self._manager.getNodeProductId(
            self._home_id, node_id)
        self._callback('zwave', 'zwave-%d' % node_id, node_info)

    if node_id in {1, 255}:
      logging.info('ZWave callback - %d %s', node_id, notification_type)
      return

    if notification_type == 'NodeAdded':
      self._node_ids.add(node_id)

      self._manager.addAssociation(self._home_id, node_id, 1, 1)
      self._manager.refreshNodeInfo(self._home_id, node_id)
      self._manager.requestNodeState(self._home_id, node_id)
      self._manager.requestNodeDynamic(self._home_id, node_id)
      self._callback('zwave', 'zwave-%d' % node_id, data)

    elif notification_type in {'ValueAdded', 'ValueChanged', 'NodeNaming'}:
      self._callback('zwave', 'zwave-%d' % node_id, data)

    else:
      logging.info('ZWave callback - %d %s', node_id, notification_type)

  @proxy.command
  def heal(self):
    self._manager.softResetController(self._home_id)
    self._manager.healNetwork(self._home_id, upNodeRoute=True)

  @proxy.command
  def heal_node(self, node_id):
    self._manager.healNetworkNode(self._home_id, node_id,
                                  upNodeRoute=True)

  @proxy.command
  def set_value(self, node_id, value_id, value):
    logging.info('Setting value %s on device %s to %s', value_id, node_id, value)
    self._manager.setValue(value_id, value)

  def stop(self):
    if self._home_id is not None:
      self._manager.writeConfig(self._home_id)
    self._manager.removeWatcher(self._callback)
    self._manager.removeDriver(self._device)
