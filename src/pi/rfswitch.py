"""rf433 device proxy code."""

import collections
import logging
import threading
import Queue

import rcswitch

from pi import proxy


class RFSwitch(proxy.Proxy):
  """433mhz RF Switch proxy implementation."""

  def __init__(self, pin, repeats=5):
    self._switch = rcswitch.RCSwitch()
    self._switch.enableTransmit(pin)

    # We repeat commands to devices, as 433Mhz switches
    # are not super reliable.
    self._repeats = repeats

    # We put commands (system code, device code, mode, repeat count)
    # on a queue, and then process them on a background thread
    # so we don't block the main event loop and can balance
    # new commands and repeats more fairy.
    self._command_queue = Queue.Queue()
    self._exiting = False
    self._command_thread = threading.Thread(target=self._command_thread_loop)
    self._command_thread.daemon = True
    self._command_thread.start()

    # To prevent repeats for a given device competeing
    # with new states for the same device, we give commands
    # generation numbers, and if we see a command for a device
    # from an old generation, we ignore it.
    self._device_command_generations = collections.defaultdict(int)

  @proxy.command
  def set_state(self, system_code, device_code, mode):
    """Handle rf swtich events - turn it on or off."""
    system_code = str(system_code)
    device_code = int(device_code)
    self._device_command_generations[(system_code, device_code)] += 1
    generation = self._device_command_generations[(system_code, device_code)]
    self._command_queue.put((system_code, device_code, mode,
                             self._repeats, generation))

  def _command_thread_loop(self):
    while not self._exiting:
      command = self._command_queue.get(True)
      if command is None:
        return

      system_code, device_code, mode, repeats, generation = command
      if generation < self._device_command_generations[
          (system_code, device_code)]:
        continue

      logging.info('system_code = %s, device_code = %s, '
                   'mode = %s, repeats = %d, generation = %d',
                   system_code, device_code, mode, repeats,
                   generation)

      if mode:
        self._switch.switchOn(system_code, device_code)
      else:
        self._switch.switchOff(system_code, device_code)

      # Put back on queue if needs repeating
      repeats -= 1
      if repeats > 0:
        self._command_queue.put((system_code, device_code, mode,
                                 repeats, generation))

  def stop(self):
    self._exiting = True
    self._command_queue.put(None)
    self._command_thread.join()
