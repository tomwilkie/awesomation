"""Tests for utils.py"""
import unittest

from common import utils


class TestUtils(unittest.TestCase):
  """."""

  def test_limit_json_batch(self):
    """Tests for limit_json_batch function."""

    self.assertEquals(list(utils.limit_json_batch([])), [])
    self.assertEquals(list(utils.limit_json_batch([1])), [[1]])

    long_string = '0' * (10 * 1000)
    self.assertEquals(list(utils.limit_json_batch([long_string])),
                      [[long_string]])
    self.assertEquals(list(utils.limit_json_batch([long_string, long_string])),
                      [[long_string], [long_string]])


if __name__ == '__main__':
  unittest.main()
