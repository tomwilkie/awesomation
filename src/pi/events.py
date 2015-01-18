"""."""
import sched
import time


SCHED = sched.scheduler(time.time, time.sleep)


def run():
  while True:
    SCHED.run()
    if SCHED.empty():
      time.sleep(10)


def enter(delay, func, args=None, priority=0):
  if args is None:
    args = []
  return SCHED.enter(delay, priority, func, args)


def cancel(event):
  SCHED.cancel(event)
