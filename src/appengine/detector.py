"""A Phi accrual failure detector."""

from time import time
from decimal import Decimal
import math

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
  threshold = 7

  def __init__(self):
    self._intervals = []
    self._hosts = {}
    self._timestamp = None

  def heartbeat(self):
    """ Call when host has indicated being alive (aka heartbeat) """
    now = time()

    if not self._timestamp is None:
      self._timestamp = time()
      return

    interval = now - self._timestamp
    self._timestamp = now
    self._intervals.append(interval)

    if len(self._intervals) > self.max_sample_size:
      self._intervals.pop(0)

    if len(self._intervals) > 1:
      self._hosts['mean'] = sum(self._intervals) / float(len(self._intervals))
      # lines below commented because deviation and variance are
      # currently unused
      #deviationsum = 0
      #for i in self._intervals[host]:
      # deviationsum += (i - self._hosts[host]['mean']) ** 2
      #variance = deviationsum / float(len(self._intervals[host]))
      #deviation = math.sqrt(variance)
      #self._hosts[host]['deviation'] = deviation

  def _probability(self, timestamp):
    # cassandra does this, citing: /* Exponential CDF = 1 -e^-lambda*x */
    # but the paper seems to call for a probability density function
    # which I can't figure out :/
    exponent = -1.0 * timestamp / self._hosts['mean']
    return 1 - (1.0 - math.pow(math.e, exponent))

  def phi(self, timestamp=None):
    if self._timestamp is None:
      return 0

    ts = timestamp
    if ts is None:
      ts = time()

    diff = ts - self._timestamp
    prob = self._probability(diff)
    if Decimal(str(prob)).is_zero():
      # a very small number, avoiding ValueError: math domain error
      prob = 1E-128
    return -1 * math.log10(prob)

  def is_alive(self):
    return self.phi() < self.threshold

  def is_dead(self):
    return not self.isAlive()
