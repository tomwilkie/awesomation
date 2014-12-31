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

The server-side logic has the concept of rooms, and when motion is sensed in a room the lights in that room are turned on.

### Architecture

[Pusher](https://pusher.com/) is used to send commands from the server app to the proxy app running on the Raspberry Pi.  Credentials for this are stored in a private subrepo; you will need to setup your own.