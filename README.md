# "Home Awesomation"

A Python 2 based home automation system.

The 'architecture' is client-server, with a Raspberry Pi based proxy running in the home and the 'logic' running in the Cloud (on Google App Engine).

Currently supports the following devices:
* ZWave motion sensors (Using the Aeon Labs Multisensor for testing)
* Philips Hue lights
* Wemo switches
* 433Mhz RF Switches (testing with [Brennenstuhl remote control mains sockets](http://www.amazon.co.uk/dp/B003BIFLSY))
* Nest Thermostats and Protects
* Netatmo weather stations
* Arbitrary wifi devices (ie your phone, for presence)

The server-side logic has the concept of rooms, and when motion is sensed in a room the lights in that room are turned on.

### Behaviours

Awesomation currently implements the following behaviours:
* If motion is sensed in a room, the lights are turned on.
* Lights are dimmed into the evening.
* If your phone is detected on the network, Nest isn't allow to enter auto-away.
* If motion is detected and your phone isn't on the network, an alert is sent.

### Architecture

The client/server model was choosen as I wanted to integrate with internet enabled apis/devices, like the Nest and Netatmo.  These APIs require pre-registered OAuth callbacks, and as far as I can tell, cannot be made to work if the callback address is different for different users.

[Pusher](https://pusher.com/) is used to send commands from the server app to the client app.  Credentials for the Pusher account are stored in a private subrepo; you will need to setup your own.

The server runs on Google App Engine; this seems to work well enough for these purposes.  The client (sometimes referred to as the proxy) runs on a Raspberry Pi in the home; an Aeon Labs Z Stick, a simple 433Mhz transmitter and a Wifi stick are connected to a USB hub, which in turn is connected to the Pi.
