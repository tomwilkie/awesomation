import sys
import urllib2
import logging
import json
import serial

from common import creds
from pusherclient import Pusher

def main():
	pusher = Pusher(creds.pusher_key)
	ser = serial.Serial('/dev/tty.usbmodem411', 9600)
	
	def sendToArduino(message):
		print message
		ser.write(message)
	
	def callback(data):
		data = json.loads(data)
		print data
		message = "%d%d\n" % (1 if data["mode"] else 0, data["num"])
		sendToArduino(message)

	def connect_handler(data):
	    channel = pusher.subscribe('test')
	    channel.bind('event', callback)
	
	pusher.connection.bind('pusher:connection_established', connect_handler)
	pusher.connect()
	pusher.connection.join()

if __name__ == '__main__':
    main()
