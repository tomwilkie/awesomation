import os
from os import path
import threading

import jsonpickle

class Store(object):

  def __init__(self, basedir):
    self._objects = {}
    self._log_file_lock = threading.Lock()
    self._log_file = open(path.join(basedir, 'commit.log'), 'ab+')

  def get(self, id):
    return self._objects.get(id, None)

  def put(self, id, obj):
    self._write_to_log(id, obj)
    self._objects[id] = obj

  def _write_to_log(self, id, obj):
    with self._log_file_lock:
      self._log_file.write(jsonpickle.encode({'id': id, 'obj': obj}))
      self._log_file.write('\n')
      self._log_file.flush()
      os.fsync(self._log_file.fileno())

  def load(self):
    with self._log_file_lock:
      for line in self._log_file:
        entry = jsonpickle.decode(line)
        self._objects(entry['id'], entry['obj'])
