"""Save version of objects to dynamodb."""
import logging
import os
import time

import boto.dynamodb2
from boto.dynamodb2 import fields
from boto.dynamodb2 import table
from boto.dynamodb2 import types
from boto.dynamodb2 import layer1

import flask

from appengine import building

# Every time we put an object to the appengine datastore,
# we're also going to save a copy to dynamodb.  This will
# allow us to graph temperature, occupied state etc over time.
#
# For this, we need to do two things: write versions,
# and read a time ordered list of versions, for a given object
# (and potentially field).
#
# Dynamodb has hash and range keys that point to an 'item' of
# keys and values.  Items can't be bigger than 400KB;
# You put 25 items per 'batch', and you get charged per
# batch put AFAICT.  Writes are more expensive than reads,
# (by 5x) and more frequent, so we probably want to
# do as much batching (and minimise the distinct
# number of items we use).  We will flush all the data
# to dynamodb at the end of each request, so we've got
# quite a bit of flexibility.
#
# We can expect every account to do ~1 write / sec.
# Read will be a couple of orders of magnitude less.
#
# Given all this, we have a couple of design choices:
#
# 0) hashkey = building_id, range key = time uid,
#    item = all the stuff flushed in this request
#
#  - 1 write per request
#  - writes would hotspot with small number of users
#  - queries will have to do a lot of work to filter
#    out the right data (ie read too much)
#
# 1) Hashkey = object id, Range key = time,
#    item = snapshot
#
#  - multiple writes per request (but less than 25?)
#  - object ids pretty random, so good distribution
#  - queries still have to do some filtering, but much
#    less
#  - single hash keys can grow infinitely large
#
# 2) Hashkey = object id + field name, range key = time,
#    item = value
#
#  - many writes per request (10 batches?)
#  - good write distribution
#  - no query filtering
#
# Given above criteria, (0) is probably the best -
# least writes, moving most of the cost query side.
# In this case I'll pick (1) though, as it'll still
# be one batch write, and queries will be easier.
# We'll extend the idea with a time bucket in the hash
# key, to stop hashes grow to large (if this is even
# a problem).


TABLE_NAME = 'history'
SCHEMA = [
    fields.HashKey('hash_key'),
    fields.RangeKey('range_key', data_type=types.NUMBER),
]
THROUGHPUT = {'read': 5, 'write': 15}
INDEXES = [
    fields.AllIndex('EverythingIndex', parts=[
        fields.HashKey('hash_key'),
        fields.RangeKey('range_key', data_type=types.NUMBER)
    ]),
]
FIELDS_TO_IGNORE = {'class', 'id', 'owner', 'last_update', 'capabilities',
                    # can't deal with repeated values yet.
                    'zwave_command_class_values', 'capabilities', 'detector'}

def get_history_table():
  """Build the history table, depending on the environment."""
  if False: #os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    logging.info('Using local dynamodb.')
    connection = layer1.DynamoDBConnection(
        region='anything',
        host='localhost',
        port=8100,
        aws_access_key_id='anything',
        aws_secret_access_key='anything',
        is_secure=False
    )
  else:
    from common import creds
    connection = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=creds.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=creds.AWS_SECRET_ACCESS_KEY,
    )

  if TABLE_NAME in connection.list_tables()['TableNames']:
    history_table = table.Table(
        TABLE_NAME,
        schema=SCHEMA,
        throughput=THROUGHPUT,
        indexes=INDEXES,
        connection=connection)
  else:
    history_table = table.Table.create(
        TABLE_NAME,
        schema=SCHEMA,
        throughput=THROUGHPUT,
        indexes=INDEXES,
        connection=connection)

  return history_table


def store_version(version):
  """Post events back to the pi."""
  batch = flask.g.get('history', None)
  if batch is None:
    batch = []
    setattr(flask.g, 'history', batch)

  building_id = building.get_id()
  batch.append((building_id, version))


def store_batch():
  """Push all the events that have been caused by this request."""
  history = flask.g.get('history', None)
  setattr(flask.g, 'history', None)
  if history is None:
    return

  logging.info('Saving %d versions to dynamodb.', len(history))

  # we might, for some reason, try and store
  # two versions of the same objects in a single
  # request.  We just drop the first in this case.
  timestamp = long(time.time() * 1000)
  items = {}

  for building_id, version in history:
    version['hash_key'] = '%s-%s-%s' % (
        building_id, version['class'], version['id'])
    version['range_key'] = timestamp
    for key in FIELDS_TO_IGNORE:
      version.pop(key, None)

    # Explictly taking copy of keys as we're mutating dict.
    # Putting a float doesn't work all the time:
    #  https://github.com/boto/boto/issues/1531
    for key in version.keys():
      value = version[key]
      if isinstance(value, (list, dict)):
        version[key] = flask.json.dumps(value)
      elif isinstance(value, float):
        del version[key]

    items[version['hash_key']] = version

  history_table = get_history_table()

  with history_table.batch_write() as batch:
    for item in items.itervalues():
      batch.put_item(data=item)


def get_range(cls, object_id, start, end):
  """Get histroic values for a given object and field."""
  building_id = building.get_id()
  history_table = get_history_table()
  values = history_table.query_2(
      hash_key__eq='%s-%s-%s' % (building_id, cls, object_id),
      range_key__gt=start,
      range_key__lte=end)

  for value in values:
    del value['hash_key']
    yield value

