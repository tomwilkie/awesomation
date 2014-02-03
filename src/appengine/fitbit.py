import json
import logging
import urllib
import urllib2

import accounts
import model

class FitbitAccount(model.Account):
  OAUTH_AUTHORISE_URL = "https://www.fitbit.com/oauth/authorize"
  OAUTH_REQUEST_TOKEN_URL = "https://api.fitbit.com/oauth/request_token"
  OAUTH_ACCESS_TOKEN_URL = "https://api.fitbit.com/oauth/access_token"
  OAUTH_CLIENT_ID = "f7f05c31ae804d2394257726b552f318"
  OAUTH_CLIENT_SECRET = "e50e8fd912b344cdb4a59b435d5a7d76"
  API_URL = "https://api.fitbit.com/"
