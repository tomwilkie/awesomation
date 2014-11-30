"""Generic device driver for 433mhz switches."""

import logging

from google.appengine.ext import ndb

from appengine import model, pushrpc


class RFSwitch(model.Device):
  """A 433mhz rf switch."""
  system_code = ndb.StringProperty(required=True)
  device_code = ndb.IntegerProperty(required=True)

  def set_value(self, value):
    event = {'type': 'rfswitch', 'system_code': self.system_code,
             'device_code': self.device_code, 'mode': value}
    pushrpc.send_event(self.owner, event)

  def handle_command(self, command):
    """Handle device commands."""
    logging.info(command)
    self.set_value(command['command'] == 'on')

