"""Represents a device on the network - used for presence."""
import logging
import re

from google.appengine.ext import ndb

from appengine import device, rest
from appengine.devices import nest


RE = re.compile(r'mac-(.*)')


@device.register('network')
class NetworkDevice(device.Device):
  """A device on the network."""
  present = ndb.BooleanProperty(required=True, default=False)

  def set_presence(self, value):
    """Set the present status of this device, and
       potentially update nest thermostats."""
    self.present = value

    # Should we set Nest to be away?
    # away = ! (big or all device)

    someone_present = False
    for presence_device in device.Device.get_by_capability('PRESENCE').iter():
      someone_present = someone_present or presence_device.present

    logging.info('Is anyone home? %s', someone_present)
    for nest_account in nest.NestAccount.query().iter():
      nest_account.set_away(not someone_present)

  @rest.command
  def fake_present(self):
    self.set_presence(True)

  @rest.command
  def fake_absent(self):
    self.set_presence(False)

  def get_capabilities(self):
    return ['PRESENCE']

  @classmethod
  def handle_static_event(cls, event):
    """Handle a device update event."""

    if 'disappeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['disappeared'])
      if network_device is None:
        return

      network_device.set_presence(False)
      network_device.put()

    elif 'appeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['appeared'])
      if network_device is None:
        return

      network_device.present.set_presence(True)
      network_device.put()

    elif 'devices' in event:
      devices = set(event['devices'])
      devices_to_put = []

      for network_device in NetworkDevice.query().iter():
        match = RE.match(network_device.key.string_id())
        assert match is not None

        mac = match.group(1)
        present = mac in devices
        if network_device.present != present:
          network_device.set_presence(present)
          devices_to_put.append(network_device)

      ndb.put_multi(devices_to_put)

