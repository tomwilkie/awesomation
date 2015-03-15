"""Generic Z Wave device driver."""

import logging

from google.appengine.ext import ndb

from appengine import device, pushrpc, rest


NODE_ADDED = 'NodeAdded'
NODE_INFO_UPDATE = 'NodeInfoUpdate'
NODE_VALUE_ADDED = 'ValueAdded'
NODE_VALUE_CHANGED = 'ValueChanged'
NODE_VALUE_REMOVED = 'ValueRemoved'

ZWAVE_DRIVERS = {}


class Driver(object):
  """A manufacture / product specific driver for a zwave device.

  NB drivers have to be stateless.  Store you state in the zwave devices.
  """
  CONFIGURATION = {}

  def __init__(self, _device):
    self._device = _device

  def _send_device_command(self, command, **kwargs):
    """Convenience method to send a command to this device."""
    event = {'type': 'zwave',
             'command': command,
             'node_id': self._device.zwave_node_id}
    event.update(kwargs)
    pushrpc.send_event(event)

  def get_capabilities(self):
    return ['HEAL']

  def get_categories(self):
    return []

  def value_changed(self, event):
    pass

  def handle_event(self, event):
    if event['notificationType'] in {NODE_ADDED, NODE_INFO_UPDATE}:
      if not self.is_configured():
        self.configure()

    elif event['notificationType'] in {NODE_VALUE_CHANGED,
                                       NODE_VALUE_ADDED}:
      self.value_changed(event)

  def is_configured(self):
    """Test if this device is configured correctly."""
    for (command_class, index), intended_value \
        in self.CONFIGURATION.iteritems():
      ccv = self._device.get_command_class_value(command_class, index)
      if ccv.value != intended_value:
        return False

    return True

  @rest.command
  def configure(self):
    """Configure this device."""
    for (command_class, index), intended_value \
        in self.CONFIGURATION.iteritems():
      ccv = self._device.get_command_class_value(command_class, index)
      if ccv.value != intended_value:
        ccv.set_value(intended_value)

  def sync(self):
    pass


def register(manufacturer_id, product_type, product_id):
  """Decorator to cause device types to be registered."""
  key = '%s-%s-%s' % (manufacturer_id, product_type, product_id)
  def class_rebuilder(cls):
    ZWAVE_DRIVERS[key] = cls
    return cls
  return class_rebuilder


class CommandClassValue(ndb.Model):
  """A particular (command class, value)."""

  command_class = ndb.StringProperty()
  index = ndb.IntegerProperty()
  value = ndb.GenericProperty()
  read_only = ndb.BooleanProperty()
  units = ndb.StringProperty()
  genre = ndb.StringProperty()
  label = ndb.StringProperty()
  value_id = ndb.IntegerProperty()
  type = ndb.StringProperty()

  def set_value(self, value):
    """Convenience method to send a command to this device."""
    event = {'type': 'zwave',
             'command': 'set_value',
             'value_id': self.value_id,
             'value': value}
    pushrpc.send_event(event)


@device.register('zwave')
class ZWaveDevice(device.Device, device.DetectorMixin):
  """Generic Z Wave device driver."""
  # pylint: disable=too-many-instance-attributes
  zwave_node_id = ndb.IntegerProperty(required=False)
  zwave_home_id = ndb.IntegerProperty(required=False)
  zwave_command_class_values = ndb.StructuredProperty(
      CommandClassValue, repeated=True)

  zwave_node_type = ndb.StringProperty()
  zwave_node_name = ndb.StringProperty()
  zwave_manufacturer_name = ndb.StringProperty()
  zwave_manufacturer_id = ndb.StringProperty()
  zwave_product_name = ndb.StringProperty()
  zwave_product_type = ndb.StringProperty()
  zwave_product_id = ndb.StringProperty()

  configured = ndb.ComputedProperty(lambda s: s.is_configured())

  # Haven't found a good way to fake out the properites yet
  brightness = ndb.IntegerProperty(default=0)
  temperature = ndb.FloatProperty(default=0.0)
  humidity = ndb.FloatProperty(default=0.0)
  lux = ndb.FloatProperty(default=0.0)

  # Represents the actual state of the switch; changing this
  # (and calling update()) will changed the switch.
  state = ndb.BooleanProperty(default=False)

  # Represents the state the user wants, and when they asked for
  # it.  Most of the time users will control rooms etc, not individual
  # lights.  But its possible.
  # UI should set this and call update_lights on the room.
  intended_state = ndb.BooleanProperty()
  state_last_update = ndb.IntegerProperty(default=0)

  def __init__(self, **kwargs):
    super(ZWaveDevice, self).__init__(**kwargs)
    self._driver = None

  def driver(self):
    """Find the zwave driver for this device."""
    if self._driver is not None:
      return self._driver

    key = '%s-%s-%s' % (self.zwave_manufacturer_id,
                        self.zwave_product_type,
                        self.zwave_product_id)
    _driver = ZWAVE_DRIVERS.get(key, None)
    if _driver is None:
      return Driver(self)
    else:
      self._driver = _driver(self)
      return self._driver

  # This is a trampoline through to the driver
  # as this class cannot implement everything
  def __getattr__(self, name):
    return getattr(self.driver(), name)

  def get_capabilities(self):
    return self.driver().get_capabilities()

  def get_categories(self):
    return self.driver().get_categories()

  def is_configured(self):
    return self.driver().is_configured()

  def get_command_class_value(self, command_class, index):
    """Find the given (command_class, index) or create a new one."""
    for ccv in self.zwave_command_class_values:
      if ccv.command_class == command_class and ccv.index == index:
        return ccv
    ccv = CommandClassValue(command_class=command_class, index=index)
    self.zwave_command_class_values.append(ccv)
    return ccv

  def handle_event(self, event):
    """Handle an event form the zwave device."""
    super(ZWaveDevice, self).handle_event(event)

    notification_type = event['notificationType']
    if 'homeId' in event:
      self.zwave_home_id = event['homeId']
    if 'nodeId' in event:
      self.zwave_node_id = event['nodeId']

    if notification_type in {NODE_VALUE_ADDED, NODE_VALUE_CHANGED}:
      # Make a copy of the value dict and mutate that
      value = dict(event['valueId'])
      command_class = value.pop('commandClass')
      index = value.pop('index')
      value['read_only'] = value.pop('readOnly')
      value['value_id'] = value.pop('id')
      del value['homeId']
      del value['nodeId']
      del value['instance']

      ccv = self.get_command_class_value(command_class, index)
      ccv.populate(**value)

      logging.info('%s.%s[%d] <- %s', self.zwave_node_id,
                   command_class, index, value)

    elif notification_type == NODE_VALUE_REMOVED:
      command_class = value.pop('commandClass')
      index = value.pop('index')
      ccv = self.get_command_class_value(command_class, index)
      self.zwave_command_class_values.remove(ccv)

      logging.info('deleted %s.%s[%d]', self.zwave_node_id,
                   command_class, index)

    elif notification_type == NODE_INFO_UPDATE:
      # event['basic']
      # event['generic']
      # event['specific']
      self.zwave_node_type = event['node_type']
      self.zwave_node_name = event['node_name']
      self.zwave_manufacturer_name = event['manufacturer_name']
      self.zwave_manufacturer_id = event['manufacturer_id']
      self.zwave_product_name = event['product_name']
      self.zwave_product_type = event['product_type']
      self.zwave_product_id = event['product_id']

    else:
      logging.info("Unknown event: %s", event)

    self.driver().handle_event(event)

  def sync(self):
    self.driver().sync()

  @classmethod
  @device.static_command
  def heal(cls):
    event = {'type': 'zwave', 'command': 'heal'}
    pushrpc.send_event(event)

  @classmethod
  @device.static_command
  def hard_reset(cls):
    event = {'type': 'zwave', 'command': 'hard_reset'}
    pushrpc.send_event(event)

  @classmethod
  @device.static_command
  def add_device(cls):
    event = {'type': 'zwave', 'command': 'add_device'}
    pushrpc.send_event(event)

  @rest.command
  def heal_node(self):
    event = {'type': 'zwave', 'command': 'heal_node',
             'node_id': self.zwave_node_id}
    pushrpc.send_event(event)
