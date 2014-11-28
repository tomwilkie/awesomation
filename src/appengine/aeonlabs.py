

class MultiSensor(zwave.Driver):
  MANUFACTUROR_ID = 86
  PRODUCT_ID = 5

  def __init__(self, device):
    device.set('COMMAND)
