"""Wemo proxy code."""

import logging

import soco

from pi import scanning_proxy


CURRENTLY_PLAYING_KEYS = ('album', 'artist', 'title')

class Sonos(scanning_proxy.ScanningProxy):
  """Sonos proxy object."""

  def __init__(self, refresh_period, callback):
    super(Sonos, self).__init__(refresh_period)

    self._callback = callback
    self._devices = {}
    self._previous_details = {}

  def _scan_once(self):
    devices = soco.discover()
    if devices is None:
      return

    devices = list(devices)

    logging.info('Found %d sonos devices.', len(devices))

    for device in devices:
      uid = device.uid
      self._devices[uid] = device

      speaker_info = device.get_speaker_info()
      currently_playing = device.get_current_track_info()
      current_transport_info = device.get_current_transport_info()

      details = {
          'uid': uid,
          'device_name': speaker_info['zone_name'],
          'currently_playing': {k: currently_playing.get(k, None)
                                for k in CURRENTLY_PLAYING_KEYS},
          'state': current_transport_info['current_transport_state'],
      }

      if self._previous_details.get(uid, None) != details:
        self._callback('sonos', 'sonos-%s' % uid, details)
        self._previous_details[uid] = details
