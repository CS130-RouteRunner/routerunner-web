"""
Route model.
"""

from google.appengine.ext import ndb


class Route(ndb.Model):
    """Model that represents a user's route from base point to dropoff point."""
    route_id = ndb.StringProperty()
    list_of_points = ndb.GeoPtProperty(repeated=True, indexed=False)
