import json
import logging
import urllib
import urllib2

import accounts
import model

class NetatmoAccount(model.Account):
  OAUTH_AUTHORISE_URL = ("https://api.netatmo.net/oauth2/authorize?"
    "client_id=%(client_id)s&redirect_uri=%(redirect_url)s&state=%(state)s")
  OAUTH_REQUEST_TOKEN_URL = "http://api.netatmo.net/oauth2/token"
  OAUTH_CLIENT_ID = "52daaaea187759c10c7b23fd"
  OAUTH_CLIENT_SECRET = "lfUPaKasvdnao2lHxpTI7kBbUvjN67wnxKCNje"
  API_URL = "http://api.netatmo.net/api/%(method)s?access_token=%(access_token)s"
  
  def DoMethod(self, method_name, **kwargs):
    url = self.API_URL % {"method": method_name, "access_token": self.oauth_access_token}
    if kwargs:
      url += "&" + urllib.urlencode(kwargs)
    logging.info(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    result = json.loads(response.read())
    assert result["status"] == "ok"
    return result["body"]
  
  def SyncDevices(self):
    devices = self.DoMethod("devicelist")
    logging.info(devices)