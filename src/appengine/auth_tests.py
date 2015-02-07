"""Test authentication."""

import unittest
import logging

import flask

from google.appengine.ext import testbed

from appengine import main


def has_no_empty_params(rule):
  defaults = rule.defaults if rule.defaults is not None else ()
  arguments = rule.arguments if rule.arguments is not None else ()
  return len(defaults) >= len(arguments)


class AuthTests(unittest.TestCase):

  def setUp(self):
    # Flask testing setup
    main.app.config['TESTING'] = True
    self.client = main.app.test_client()

    # Appengine testing setup
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_user_stub()

  def tearDown(self):
    self.testbed.deactivate()

  def testEndpointsReturn401(self):
    """Test all endpoints needs authentication."""

    for rule in main.app.url_map.iter_rules():
      logging.debug('Testing endpoint "%s"', rule.endpoint)

      # special case static files, no auth..
      if rule.endpoint == 'static':
        continue

      # User a dummy object_id on endpoints
      # that need on, just to construct a URL
      if rule.arguments == set():
        arguments = {}
      if rule.arguments == set(['object_id']):
        arguments = {'object_id': '12345'}
      elif not has_no_empty_params(rule):
        logging.error(rule.arguments)
        assert False

      with main.app.test_request_context():
        url = flask.url_for(rule.endpoint, **arguments)

      logging.debug('  url = "%s"', url)

      # Only 2 special cases cause redirects - only human endpoints
      if rule.endpoint in {'root', 'user.use_invite'}:
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        continue

      # Filter out rules we can't navigate to in a browser
      # and rules that require parameters
      if 'GET' in rule.methods:
        response = self.client.get(url)
        self.assertEquals(response.status_code, 401)

      if 'POST' in rule.methods:
        response = self.client.post(url)
        self.assertEquals(response.status_code, 401)

      if 'DELETE' in rule.methods:
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 401)


if __name__ == '__main__':
  unittest.main()
