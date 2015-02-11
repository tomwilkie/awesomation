"""Base classes for my data model."""
import decimal

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from appengine import history, rest, user


# From http://stackoverflow.com/questions/10035133/ndb-decimal-property
class DecimalProperty(ndb.IntegerProperty):
  """Decimal property ideal to store currency values, such as $20.34."""
  # See https://developers.google.com/appengine/docs/python/ndb/subclassprop
  def _validate(self, value):
    if not isinstance(value, (decimal.Decimal, str, unicode, int, long)):
      raise TypeError('Expected a Decimal, str, unicode, int '
                      'or long an got instead %s' % repr(value))

  def _to_base_type(self, value):
    return int(decimal.Decimal(value) * 100)

  def _from_base_type(self, value):
    return decimal.Decimal(value)/decimal.Decimal(100)


class Base(polymodel.PolyModel):
  """Base for all objects."""

  def to_dict(self):
    """Convert this object to a python dict."""
    result = super(Base, self).to_dict()
    result['id'] = self.key.id()
    result['class'] = result['class_'][-1]
    del result['class_']

    # Should move this into detector mixin when I figure out how
    if 'detector' in result:
      del result['detector']
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
  def get_history(self, start, end):
    values = self.to_dict()
    return history.get_range(values['class'], values['id'],
                             start, end)

  def sync(self):
    """Called when fields on the object are updated
       through the API."""
    pass
