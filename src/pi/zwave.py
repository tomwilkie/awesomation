import logging

import libopenzwave

class ZWave(object):
  
  def __init__(self, device):
    self._device = device
    
    self._options = libopenzwave.PyOptions()
    self._options.create(
      libopenzwave.configPath(), '.', '')
    self._options.addOptionBool("ConsoleOutput", False)
    self._options.lock()
    
    self._manager = libopenzwave.PyManager()
    self._manager.create()
    self._manager.addWatcher(self._Callback)
    self._manager.addDriver(self._device)

  def _Callback(self, data):
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

  def HandleEvent(self, event):
    pass

  def Stop(self):
    self._manager.stop()
