"""
UserSession model.
"""

from google.appengine.ext import ndb


class UserSession(ndb.Model):
    """Model that represents a single users's data for a single game."""
    user_session_id = ndb.StringProperty()
    base_point = ndb.GeoPtProperty()
    drop_off_point = ndb.GeoPtProperty()
    user_current_gold = ndb.StringProperty()
    route_id = ndb.StringProperty()
