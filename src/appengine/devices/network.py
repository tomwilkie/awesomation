"""Represents a device on the network - used for presence."""

import re

from google.appengine.ext import ndb

from appengine import device


RE = re.compile(r'mac-(.*)')


@device.register('network')
class NetworkDevice(device.Device):
  """A device on the network."""
  present = ndb.BooleanProperty(required=True, default=False)

  @classmethod
  def handle_static_event(cls, event):
    """Handle a device update event."""

    if 'disappeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['disappeared'])
      if network_device is None:
        return

      network_device.present = False
      network_device.put()

    elif 'appeared' in event:
      network_device = NetworkDevice.get_by_id('mac-%s' % event['appeared'])
      if network_device is None:
        return

      network_device.present = True
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
          devices_to_put.append(network_device)

      ndb.put_multi(devices_to_put)

