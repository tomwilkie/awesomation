"""Tests for detector.py"""
import unittest

from common import detector


class TestDetector(unittest.TestCase):
  """."""

  def test_new_detector(self):
    """."""

    dtor = detector.AccrualFailureDetector()
    dtor.heartbeat()
    self.assertTrue(dtor.is_alive())


if __name__ == '__main__':
  unittest.main()
