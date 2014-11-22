import libopenzwave

class ZWave(object):
  
  def __init__(self, device):
    self._device = device
    
    self._options = libopenzwave.PyOptions()
    self._options.create(
      libopenzwave.configPath(), '.', '')
    self._options.lock()
    
    self._manager = libopenzwave.PyManager()
    self._manager.create()
    self._manager.addWatcher(self._Callback)
    self._manager.addDriver(self._device)

  def _Callback(self, args):
    print args
