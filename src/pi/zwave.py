import libopenzwave

class ZWave(object):
  
  def __init__(self, device):
    self._device = device
    manager = libopenzwave.PyManager()
    manager.create()
    manager.addWatcher(self._Callback)
    manager.addDriver(self._device)

  def _Callback(self, args):
    print args
