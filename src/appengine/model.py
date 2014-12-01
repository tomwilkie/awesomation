"""Base classes for my data model."""

from google.appengine.ext.ndb import polymodel


class Base(polymodel.PolyModel):

  def to_dict(self):
    """Convert this object to a python dict."""
    result = super(Base, self).to_dict()
    result['id'] = self.key.id()
    result['class'] = result['class_'][-1]
    del result['class_']
    return result

