""" Remove a property from the datastore.
How to use:

$ cd experimental/db/
$ PYTHONPATH=. remote_api_shell.py -s homeawesomation.appspot.com
> import remove_property
"""

from google.appengine.api import namespace_manager
from google.appengine.ext import db

class Base(db.Expando): pass

def remove(namespace, field):
  namespace_manager.set_namespace(namespace)
  for base in Base.all().run():
    if hasattr(base, field):
      print "%s %s" % (base.key().id_or_name(), getattr(base, 'name', None))
      delattr(base, field)
      base.put()
