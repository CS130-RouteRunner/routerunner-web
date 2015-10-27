"""
User model.
"""
from google.appengine.ext import ndb


class User(ndb.Model):
    """Model that represents a single User."""
    # User profile
    google_id = ndb.StringProperty()
    email = ndb.StringProperty()
    # Unique id provided by PubNub
    uuid = ndb.StringProperty()
    # In-game name of user
    nickname = ndb.StringProperty(indexed=False)

    # Statistics
    win = ndb.IntegerProperty(indexed=False)
    loss = ndb.IntegerProperty(indexed=False)
    # Average game length in minutes
    avg_game_duration = ndb.IntegerProperty(indexed=False)
