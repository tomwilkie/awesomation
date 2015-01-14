"""Base classes for my data model."""
from google.appengine.ext.ndb import polymodel

from appengine import history, rest, user


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
      values = self.to_dict()
      user.send_event(cls=classname, id=self.key.string_id(),
                      event='update', obj=values)
      history.store_version(values)
    return super(Base, self)._put_async(**ctx_options)
  put_async = _put_async

  @rest.command
  def get_history(self, field, start, end):
    values = self.to_dict()
    return history.get_range(values['class'], values['id'],
                             start, end, field)

  def sync(self):
    """Called when fields on the object are updated
       through the API."""
    pass
