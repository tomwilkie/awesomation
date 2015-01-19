"""Represents a device on the network - used for presence."""
import logging
import re

from google.appengine.ext import ndb

from appengine import device
from appengine.devices import nest


RE = re.compile(r'mac-(.*)')


@device.register('network')
class NetworkDevice(device.Device):
  """A device on the network."""
  present = ndb.BooleanProperty(required=True, default=False)

  @staticmethod
  def update_presence():
    """Set the present status of this device, and
       potentially update nest thermostats."""
    # Should we set Nest to be away?
    # away = ! (big or all device)

    someone_present = False
    for presence_device in device.Device.get_by_capability('PRESENCE').iter():
      someone_present = someone_present or presence_device.present

    logging.info('Is anyone home? %s', someone_present)
    for nest_account in nest.NestAccount.query().iter():
      nest_account.set_away(not someone_present)

  def sync(self):
    self.update_presence()

  def get_capabilities(self):
    return ['PRESENCE']

  @classmethod
  def handle_static_event(cls, event):
    """Handle a device update event."""

    if 'disappeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['disappeared'])
      if network_device is None:
        return

      network_device.present = False
      network_device.update_presence()
      network_device.put()

    elif 'appeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['appeared'])
      if network_device is None:
        return

      network_device.present = True
      network_device.update_presence()
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
          network_device.present = present
          network_device.update_presence()
          devices_to_put.append(network_device)

      ndb.put_multi(devices_to_put)

