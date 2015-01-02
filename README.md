# "Home Awesomation"

A Python 2 based home automation system.

The 'architecture' is client-server, with a Raspberry Pi based proxy running in the home and the 'logic' running in the Cloud (on appengine).

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
* If your phone is detected on the network, Nest isn't allow to enter auto-away.
* If motion is detected and your phone isn't on the network, an alert is sent.

### Architecture

The client/server model was choosen as I wanted to integrate with internet enabled apis/devices, like the Nest and Netatmo.  These APIs require pre-registered OAuth callbacks, and as far as I can tell, cannot be made to work if the callback address is different for different users.

[Pusher](https://pusher.com/) is used to send commands from the server app to the proxy app running on the Raspberry Pi.  Credentials for this are stored in a private subrepo; you will need to setup your own.
