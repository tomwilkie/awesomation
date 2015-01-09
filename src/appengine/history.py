import time

import boto.dynamodb2
from boto.dynamodb2 import fields
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

from common import creds


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
# 0) hashkey = user_id, range key = time uid,
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
    fields.HashKey('class_object', data_type=NUMBER),
    fields.RangeKey('time'),
]
THROUGHPUT = {'read': 5, 'write': 15}
INDEXES = [
    fields.AllIndex('EverythingIndex'),
    fields.HashKey('account_type', data_type=NUMBER),
]
CONNECTION = boto.dynamodb2.connect_to_region(
    region='us-east-1',
    aws_access_key_id=creds.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=creds.AWS_SECRET_ACCESS_KEY,
)


FIELDS_TO_IGNORE = {'class', 'id', 'owner', 'last_update', 'capabilities'}


HISTORY_TABLE = Table.create(
  TABLE_NAME,
  schema=SCHEMA,
  throughput=THROUGHPUT,
  indexes=INDEXES,
  connection=CONNECTION)


def store_version(values):
  user_id = None
  hash_key = "%s-%s-%s" % (user_id, values['class'], values['id'])
  dt = time.time()

  values = []
