"""Generic device driver for 433mhz switches."""

import logging

from google.appengine.ext import ndb

from appengine import model, pushrpc


class RFSwitch(model.Device):
  system_code = ndb.StringProperty(required=True)
  device_code = ndb.IntegerProperty(required=True)

  def handle_command(self, command):
    """Handle device commands."""
    logging.info(command)

    event = {'type': 'rfswitch', 'system_code': self.system_code,
             'device_code': self.device_code}
    if command['command'] == 'on':
      event['mode'] = True
    else:
      event['mode'] = False

    pushrpc.send_event(self.owner, event)
