import threading
import Queue


class Batcher(object):
  """Encapsultes a queue for batching up objects."""

  def __init__(self, on_batch, max_batch_size=20):
    self._on_batch = on_batch
    self._max_batch_size = max_batch_size

    self._queue = Queue.Queue()
    self._exiting = False
    self._flush_thread = threading.Thread(target=self._flush_loop)
    self._flush_thread.start()

  def queue(self, obj):
    self._queue.put(event)

  def stop(self):
    self._exiting = True
    self._flush_thread.put(None)
    self._flush_thread.join()

  def _get_batch(self):
    """Retrieve as many events from queue as possible without blocking."""
    batch = []
    while len(batch) < self._max_batch_size:
      try:
        # First time round we should wait (when list is empty)
        block = len(batch) == 0
        obj = self._queue.get(block)

        # To break out of this thread, we inject a None event in stop()
        if obj is None:
          return None

        batch.append(obj)
      except Queue.Empty:
        break

    assert events
    return events

  def _flush_loop(self):
    while not self._exiting:
      batch = self._get_batch()
      if batch is None:
        break

      # pylint: disable=broad-except
      try:
        self._on_batch(batch)
      except Exception:
        logging.error('Exception processing batch',
                      exc_info=sys.exc_info())
