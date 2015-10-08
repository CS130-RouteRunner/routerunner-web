"""
Song model.
"""
import json
from google.appengine.ext import ndb


class Song(ndb.Model):
    """Model that represents a single Song entry."""
    title = ndb.StringProperty()
    artist = ndb.StringProperty()
    duration = ndb.StringProperty()
    genre = ndb.StringProperty()

    def to_json(self):
        """Returns Song model in JSON form"""
        return json.dumps(dict([(p, unicode(getattr(self, p))) for p in self._properties]))
