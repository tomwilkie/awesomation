from google.appengine.api import namespace_manager

class Base(db.Expando): pass

for namespace in namespace_manager.list_namespaces():
  namespace_manager.set_namespace(namespace)
  for base in Base.all().run():
    if hasattr(base, 'category'):
      del base.category
      base.put()
