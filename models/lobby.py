"""
Lobby model for pregame purposes.
"""
from google.appengine.ext import ndb


class Lobby(ndb.Model):
    """Model that represents a single Lobby."""
    # PubNub channel id
    lobby_id = ndb.StringProperty()
    # String list of user id's
    users = ndb.StringProperty(repeated=True, indexed=False)
    # String list of users who are ready to play the game
    ready = ndb.StringProperty(repeated=True, indexed=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    started = ndb.BooleanProperty(default=False)
