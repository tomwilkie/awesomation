# Python Client for GAE Channel API

A python client implementation for 
[Google Appengine Channel API](http://code.google.com/appengine/docs/python/channel/overview.html).

Google only provides a javascript client, while I needed long polls using
a python client. So I reverse engineered the protocol and implemented it 
in python.

It seems to work, though it's not well
tested yet. Be aware that google could change the underlying protocol without any
notice. The best thing you can expect in such a case is to get ChannelError
exception. But it could also just stop workin in some other way.
You've been warned.

## Usage

    import gae_channel

    channel = gae_channel.Client(token='your channel token')
    for msg in chan.messages():
        print msg

## Demo
Also have a look at /demo. There's a small demo client.

    $ python receiver.py 
    Your channel name is: fWVwdXvNJP
    now run in an other terminal:
    python sender.py fWVwdXvNJP
    I'm now listening for messages, dont close this terminal...

Now in another terminal, run:

    $ python sender.py fWVwdXvNJP
    Enter a message:test

Now you'll see the message in the first terminal:

    Message received: test


