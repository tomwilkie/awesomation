
event_callback = None

def send_event(event):
  if event_callback == None:
    return

  event_callback(event)
