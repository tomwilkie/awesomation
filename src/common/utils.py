"""Bunch of random util functions."""
import flask


def limit_json_batch(events, max_size=10240):
  """Given a list of stuff, yeild json encoded lists
     of length less than max_size."""

  # First lets go through and encode all the events
  events = [flask.json.dumps(event) for event in events]
  start = 0
  end = 0
  acc = 2 # start and end braces

  while end < len(events):
    event_length = len(events[end])

    # +1 for comma
    if acc + event_length + 1 < max_size:
      end += 1
      acc += event_length + 1
      continue

    # we have to yeild start..end, and they can't be the same
    assert start < end, 'Single event too big'

    result = '[%s]' % (','.join(events[start:end]))
    assert len(result) < max_size
    yield result
    start = end
    acc = 2

  assert start <= end
  if start != end:
    result = '[%s]' % (','.join(events[start:end]))
    assert len(result) < max_size
    yield result
