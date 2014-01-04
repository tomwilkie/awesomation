import sys
import urllib2
import logging
import json
import serial
import serial.tools.list_ports

from common import creds
from pusherclient import Pusher

def find_arduino():
    # These are the vendor and product ids for the 
    # arduino's ftdi chip, I think
	ports = list(serial.tools.list_ports.grep(r'VID:PID=2341:43'))
	if not ports:
		sys.stderr.write("No Arduino found.\n")
		sys.exit(-1)
	if len(ports) > 1:
		sys.stderr.write("Too many Arduino's found.\n")
		sys.exit(-1)
	return ports[0][0]

def main():
	pusher = Pusher(creds.pusher_key)
	ser = serial.Serial(find_arduino(), 9600)
	
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
	
	pusher.connection.bind('pusher:connection_established',
	    connect_handler)
	pusher.connect()
	pusher.connection.join()

if __name__ == '__main__':
    main()
