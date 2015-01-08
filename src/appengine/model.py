"""Base classes for my data model."""
from google.appengine.ext.ndb import polymodel

from appengine import user


class Base(polymodel.PolyModel):
  """Base for all objects."""

  def to_dict(self):
    """Convert this object to a python dict."""
    result = super(Base, self).to_dict()
    result['id'] = self.key.id()
    result['class'] = result['class_'][-1]
    del result['class_']
    return result

  @classmethod
  def _event_classname(cls):
    return None

  def _put_async(self, **ctx_options):
    """Overrides _put_async and sends event to UI."""
    classname = self._event_classname()
    if classname is not None:
      user.send_event(cls=classname, id=self.key.string_id(),
                      event='update', obj=self.to_dict())
    return super(Base, self)._put_async(**ctx_options)
  put_async = _put_async
