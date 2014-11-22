import json

from common import creds
from pusherclient import Pusher


def Start():
    pusher = Pusher(creds.pusher_key)

    def callback(data):
        try:
            data = json.loads(data)
            print data
            
        except Exception, e:
            print e
            traceback.print_exc()

    def connect_handler(data):
        channel = pusher.subscribe('test')
        channel.bind('event', callback)

    pusher.connection.bind('pusher:connection_established',
        connect_handler)
    pusher.connect()

    while True:
        time.sleep(100)