"""Local proxy objects."""

import abc
import logging


def command(func):
  func.is_command = True
  return func


class Proxy(object):
  """Abstract base class for local proxy objects."""
  __metaclass__ = abc.ABCMeta

  def handle_command(self, cmd):
    """Handle a command for this proxy"""
    command_name = cmd.pop('command')

    command_method = getattr(self, command_name, None)
    if command_method is None or not command_method.is_command:
      logging.error('"%s" is not a valid command for a %s',
                    command_name, self.__class__.__name__)
      return

    command_method(**cmd)

  @abc.abstractmethod
  def stop(self):
    pass

  @abc.abstractmethod
  def join(self):
    pass
