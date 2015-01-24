"""Building abstraction."""

from google.appengine.api import namespace_manager

# Buildings don't exist per se - we just store the building ID in the namespace

def get_id():
  namespace = namespace_manager.get_namespace()
  assert namespace != ''
  return namespace
