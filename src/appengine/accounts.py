import json
import logging
import random
import string
import urllib
import urllib2

import model
import netatmo

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


def RefreshToken(self):
  code = self.request.get("code")
  url = self.OAUTH_REQUEST_TOKEN_URL
  form_data = {
    "grant_type": "refresh_token",
    "client_id": self.OAUTH_CLIENT_ID,
    "client_secret": self.OAUTH_CLIENT_SECRET,
    "refresh_token": self.refresh_token,
  }
  response = Post(url, form_body=form_data)
  data = json.loads(response.read())
  self.access_token = data["access_token"]
  self.refresh_token = data["refresh_token"]
  self.put()


def RandomString(length):
  return ''.join(random.choice(string.ascii_letters) for x in xrange(length))


def Post(url, form_body=None, body=None, headers={}):
  assert form_body is not None or body is not None
  request_data = body if body is not None else urllib.urlencode(form_body)
  if form_body is not None:
      headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
  request = urllib2.Request(url, data=request_data, headers=headers)
  response = urllib2.urlopen(request)
  return response.read()


class DevicesEndpoint(webapp.RequestHandler):
  @util.login_required
  def get(self, account_id):
    user = users.get_current_user()
    account = model.Account.get_by_id(int(account_id))
    assert account.owner == user.user_id()
    
    account.SyncDevices()
    

class AccountEndpoint(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    assert user is not None
    
    q = db.GqlQuery("SELECT * FROM Account WHERE owner = :1", user.user_id())
    result = q.run(limit = 5)
    
    self.response.write(json.dumps([db.to_dict(r) for r in result]))
  
  def post(self):
    user = users.get_current_user()
    assert user is not None
    params = json.loads(self.request.body)
    account_type = params["type"]
    if account_type == "netatmo":
      account = netatmo.NetatmoAccount(owner=user.user_id())
    else:
      assert False
    account.put()
    self.response.out.write(json.dumps({"id": account.key().id()}))


class OAuthRedirect(webapp.RequestHandler):
  @util.login_required
  def get(self, account_id):
    user = users.get_current_user()
    account = model.Account.get_by_id(int(account_id))
    assert account.owner == user.user_id()
    
    account.oauth_state = RandomString(10)
    account.put()
    
    redirect_url = "http://%s/api/account/%s/callback" % (self.request.host, account_id)
    
    logging.info("Redirecting to: %s", redirect_url)
    
    self.redirect(account.OAUTH_AUTHORISE_URL % {
      "state": account.oauth_state,
      "client_id": account.OAUTH_CLIENT_ID, 
      "redirect_url": redirect_url})


class OAuthCallback(webapp.RequestHandler):
  def get(self, account_id):
    account = model.Account.get_by_id(int(account_id))
    state = self.request.get("state")
    assert state == account.oauth_state
    account.oauth_state = None
    
    code = self.request.get("code")
    url = account.OAUTH_REQUEST_TOKEN_URL
    redirect_url = "http://%s/api/account/%s/callback" % (
      self.request.host, account_id)
    form_data = {
      "grant_type": "authorization_code",
      "client_id": account.OAUTH_CLIENT_ID,
      "client_secret": account.OAUTH_CLIENT_SECRET,
      "code": code,
      "redirect_uri": redirect_url,
    }
    response = Post(url, form_body=form_data)
    data = json.loads(response)
    logging.info(data)
    account.oauth_access_token = data["access_token"]
    account.oauth_refresh_token = data["refresh_token"]
    account.put()
    logging.info(db.to_dict(account))
    
    self.response.out.write("<html><body>done</body></html>")


endpoints = [
  ("/api/account", AccountEndpoint),
  ("/api/account/(\d+)/redirect", OAuthRedirect),
  ("/api/account/(\d+)/callback", OAuthCallback),
  ("/api/account/(\d+)/devices", DevicesEndpoint)]
