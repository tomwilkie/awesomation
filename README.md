## "Home Awesomation"

A Python 2 based home automation system.

The 'architecture' is client-server, with a Raspberry Pi based proxy running in the home and the 'logic' running in the Cloud (on appengine).

Currently supports the following devices:
* ZWave motion sensors (Using the Aeon Labs Multisensor for testing)
* Philips Hue lights
* Wemo switches
* RF Switched (433Mhz - testing with http://www.amazon.co.uk/dp/B003BIFLSY)

The server-side logic has the concept of rooms, and when motion is sensed in a room the lights in that room are turned on.
