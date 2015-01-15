"""Bunch of random util functions."""
import flask


def limit_json_batch(events, max_size=10240):
  """Given a list of stuff, yeild lists of stuff
     which, when json encoded, would be
     of length less than max_size."""

  # First lets go through and encode all the events
  encoded_events = [flask.json.dumps(event) for event in events]
  start = 0
  end = 0
  acc = 2 # start and end braces

  while end < len(encoded_events):
    event_length = len(encoded_events[end])
    assert event_length < max_size, encoded_events[end]

    # +1 for comma
    if acc + event_length + 1 < max_size:
      end += 1
      acc += event_length + 1
      continue

    # we have to yeild start..end, and they can't be the same
    assert start < end

    result = '[%s]' % (','.join(encoded_events[start:end]))
    assert len(result) < max_size
    yield events[start:end]
    start = end
    acc = 2

  assert start <= end
  if start != end:
    result = '[%s]' % (','.join(encoded_events[start:end]))
    assert len(result) < max_size
    yield events[start:end]
