"""A Phi accrual failure detector."""
import decimal
import logging
import math
import sys
import time


class AccrualFailureDetector(object):
  """ Python implementation of 'The Phi Accrual Failure Detector'
  by Hayashibara et al.

  * Taken from https://github.com/rschildmeijer/elastica/blob/
    a41f9427f80b5207891597ec430e76949e4948df/elastica/afd.py
  * Licensed under under Apache version 2 according to the README.rst.
  * Original version by Brandon Williams (github.com/driftx)
  * modified by Roger Schildmeijer (github.com/rchildmeijer))

  Failure detection is the process of determining which nodes in
  a distributed fault-tolerant system have failed. Original Phi
  Accrual Failure Detection paper: http://ddg.jaist.ac.jp/pub/HDY+04.pdf

  A low threshold is prone to generate many wrong suspicions but
  ensures a quick detection in the event of a real crash. Conversely,
  a high threshold generates fewer mistakes but needs more time to
  detect actual crashes.

  We use the algorithm to self-tune sensor timeouts for presence.
  """

  max_sample_size = 1000
  # 1 = 10% error rate, 2 = 1%, 3 = 0.1%.., (eg threshold=3. no
  # heartbeat for >6s => node marked as dead
  threshold = 3

  def __init__(self):
    self._intervals = []
    self._mean = 60
    self._timestamp = None

  @classmethod
  def from_dict(cls, values):
    detector = cls()
    detector._intervals = values['intervals']
    detector._mean = values['mean']
    detector._timestamp = values['timestamp']
    return detector

  def to_dict(self):
    return {
        'intervals': self._intervals,
        'mean': self._mean,
        'timestamp': self._timestamp
    }

  def heartbeat(self, now=None):
    """ Call when host has indicated being alive (aka heartbeat) """
    if now is None:
      now = time.time()

    if self._timestamp is None:
      self._timestamp = now
      return

    interval = now - self._timestamp
    self._timestamp = now
    self._intervals.append(interval)

    if len(self._intervals) > self.max_sample_size:
      self._intervals.pop(0)

    if len(self._intervals) > 0:
      self._mean = sum(self._intervals) / float(len(self._intervals))
      logging.debug('mean =  %s', self._mean)

  def _probability(self, diff):
    if self._mean == 0:
      # we've only seen one heartbeat
      # so use a different formula
      # for probability
      return sys.float_info.max

    # cassandra does this, citing: /* Exponential CDF = 1 -e^-lambda*x */
    # but the paper seems to call for a probability density function
    # which I can't figure out :/
    exponent = -1.0 * diff / self._mean
    return 1 - (1.0 - math.pow(math.e, exponent))

  def phi(self, timestamp=None):
    if self._timestamp is None:
      # we've never seen a heartbeat,
      # so it must be missing...
      return self.threshold

    if timestamp is None:
      timestamp = time.time()

    diff = timestamp - self._timestamp
    prob = self._probability(diff)
    logging.debug('Proability = %s', prob)
    if decimal.Decimal(str(prob)).is_zero():
      # a very small number, avoiding ValueError: math domain error
      prob = 1E-128
    return -1 * math.log10(prob)

  def is_alive(self, timestamp=None):
    phi = self.phi(timestamp)
    logging.debug('Phi = %s', phi)
    return phi < self.threshold

  def is_dead(self, timestamp=None):
    return not self.is_alive(timestamp)
