import time
import apns

CERT_FILE='dist/door/DomicsCert.pem'
KEY_FILE='dist/door/DomicsKey.pem'
DEVICE_TOKEN='a6ad1275b3b8443aa9472244ae63c3826de937cd64c6e0ee837acaf7ccd6f91e'

instance = apns.APNs(use_sandbox=True, cert_file=CERT_FILE, key_file=KEY_FILE)

def SendNotification():
  # Send a notification
  payload = apns.Payload(alert="Hello World!", sound="default", badge=1)
  instance.gateway_server.send_notification(DEVICE_TOKEN, payload)
