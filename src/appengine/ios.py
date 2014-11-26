import time

#import apns

from google.appengine.ext import db

from appengine import model

CERT_FILE='dist/door/DomicsCert.pem'
KEY_FILE='dist/door/DomicsKey.pem'


class IosDevice(model.Device):
  push_token = db.StringProperty(required=False)

  def __init__(self, **kwargs):
    self.apns = apns.APNs(use_sandbox=True, cert_file=CERT_FILE, key_file=KEY_FILE)

  def SendNotification(notification):
    """Send a notification to this iOS device."""
    payload = apns.Payload(alert=notification, sound="default", badge=1)
    self.apns.gateway_server.send_notification(self.push_token, payload)
