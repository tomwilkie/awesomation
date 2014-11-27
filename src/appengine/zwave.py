"""Generic Z Wave device driver."""

import logging

from google.appengine.ext import ndb

from appengine import model


class CommandClassValue(ndb.Model):
  """A particular (command class, value)."""

  command_class = ndb.StringProperty()
  index = ndb.IntegerProperty()
  value = ndb.GenericProperty()
  read_only = ndb.BooleanProperty()
  units = ndb.StringProperty()
  genre = ndb.StringProperty()
  label = ndb.StringProperty()
  type = ndb.StringProperty()


class ZWaveDevice(model.Device):
  """Generic Z Wave device driver."""
  zwave_node_id = ndb.IntegerProperty(required=False)
  zwave_home_id = ndb.IntegerProperty(required=False)
  zwave_command_class_values = ndb.StructuredProperty(
      CommandClassValue, repeated=True)

  def __init__(self, **kwargs):
    super(ZWaveDevice, self).__init__(**kwargs)

  def _command_class_value(self, command_class, index):
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
    self.zwave_home_id = event['homeId']
    self.zwave_node_id = event['nodeId']

    if notification_type in {'ValueAdded', 'ValueChanged'}:
      value = event['valueId']
      command_class = value.pop('commandClass')
      index = value.pop('index')
      value['read_only'] = value['readOnly']
      del value['homeId']
      del value['nodeId']
      del value['readOnly']
      del value['instance']
      del value['id']

      ccv = self._command_class_value(command_class, index)
      ccv.populate(**value)

      logging.info('%s.%s[%d] <- %s', self.zwave_node_id,
                   command_class, index, value)

    elif notification_type == 'NodeNaming':
      logging.info(event)

