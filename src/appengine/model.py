"""Base classes for my data model."""
import decimal

from appengine import history, rest, user

class Property(object):
  def __init__(self, default=None):
    self._name = None
    self._default = default

  def get_default(self):
    return self._default

  def get_value(self, instance):
    return instance.__dict__.get(self._name, self._default)

class ComputedProperty(object):
  def __init__(self, f):
    self._f = f

  def get_default(self):
    return self._f()

  def get_value(self, instance):
    return self._f()

class MetaModel(type):
  def __init__(cls, name, bases, classdict):
    super(MetaModel, cls).__init__(name, bases, classdict)

    cls._properties = {}  # Map of {name: Property}
    for name in set(dir(cls)):
      attr = getattr(cls, name, None)
      if isinstance(attr, Property):
        attr._name = name
        cls._properties[attr._name] = attr

class Base(object):
  """Base for all objects."""
  __metaclass__ = MetaModel
  _properties = None
  _store = None

  @classmethod
  def set_store(cls, store):
    cls._store = store

  def __init__(self, id, **kwargs):
    self.id = id
    self.populate(**kwargs)

  def populate(self, **kwargs):
    for k, v in kwargs.iteritems():
      prop = getattr(self.__class__, k)
      self.__dict__[k] = v
    # init defaults
    for k, prop in self.__class__._properties.iteritems():
      if k in kwargs: continue
      self.__dict__[k] = prop.get_default()

  def to_dict(self):
    """Convert this object to a python dict."""
    result = {"id": self.id, "class": self.__class__.name}
    for propname in self.__class__._properties.iterkeys():
      result[propname] = self.__dict__.get(propname, None)
    return result

  @classmethod
  def _event_classname(cls):
    return None

  @classmethod
  def get_by_id(cls, id):
    return cls._store.get(id)

  def put(self):
    """Overrides _put_async and sends event to UI."""
    Base._store.put(self.id, self)
    classname = self._event_classname()
    if classname is not None:
      values = self.to_dict()
      user.send_event(cls=classname, id=self.id,
                      event='update', obj=values)
      history.store_version(values)

  @rest.command
  def get_history(self, start, end):
    values = self.to_dict()
    return history.get_range(values['class'], values['id'],
                             start, end)

  def sync(self):
    """Called when fields on the object are updated
       through the API."""
    pass
