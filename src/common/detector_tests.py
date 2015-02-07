"""Tests for detector.py"""
import logging
import unittest

from common import detector


class TestDetector(unittest.TestCase):
  """."""

  def test_new_detector(self):
    """."""

    dtor = detector.AccrualFailureDetector()
    self.assertTrue(dtor.is_dead(timestamp=0))

    dtor.heartbeat(now=0)
    self.assertTrue(dtor.is_alive(timestamp=1))

    # check the detector is off after an hour
    self.assertTrue(dtor.is_dead(timestamp=7 * 60))

  def test_intermittent(self):
    def test_at_interval(interval):
      logging.debug('Testing at %d intervals', interval)
      dtor = detector.AccrualFailureDetector()
      dtor.heartbeat(now=0)
      dtor.heartbeat(now=interval)

      for i in xrange(2, 100):
        dt = i*interval
        logging.debug('Testing alive at %d', dt)
        self.assertTrue(dtor.is_alive(timestamp=dt))
        dtor.heartbeat(now=dt)

      dt = 107 * interval
      logging.debug('Testing dead at %d', dt)
      self.assertTrue(dtor.is_dead(timestamp=dt))

    for i in xrange(1, 20):
      test_at_interval(i*60)

  def test_ramp(self):
    dt = 0
    dtor = detector.AccrualFailureDetector()
    dtor.heartbeat(now=dt)

    for i in xrange(1, 30):
      dt += i * 60
      logging.debug('Is alive at %d', dt)
      self.assertTrue(dtor.is_alive(timestamp=dt))
      dtor.heartbeat(now=dt)

    # will have learnt an average interval of 15mins

    dt += 7 * 15 * 60
    logging.debug('Is dead at %d', dt)
    self.assertTrue(dtor.is_dead(timestamp=dt))


if __name__ == '__main__':
  unittest.main()
