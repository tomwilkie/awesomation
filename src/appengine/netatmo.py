import model

class WeatherStation(model.Device):
  OAUTH_AUTHORISE_URL = ("https://api.netatmo.net/oauth2/authorize?"
    "client_id=%{client_id}s&redirect_uri=%{redirect_url}s&state=%{state}s")
  OAUTH_REQUEST_TOKEN_URL = "http://api.netatmo.net/oauth2/token"
  OAUTH_CLIENT_ID = "52daaaea187759c10c7b23fd"
  OAUTH_CLIENT_SECRET = "lfUPaKasvdnao2lHxpTI7kBbUvjN67wnxKCNje"