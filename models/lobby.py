"""
Lobby model for pregame purposes.
"""
from google.appengine.ext import ndb


class Lobby(ndb.Model):
    """Model that represents a single Lobby."""
    channel_id = ndb.StringProperty()
    # String list of user id's
    users = ndb.StringProperty(repeated=True)
