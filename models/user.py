"""
User model.
"""
from google.appengine.ext import ndb


class User(ndb.Model):
    """Model that represents a single User."""
    # Unique id for pubnub
    uuid = ndb.StringProperty()
    nickname = ndb.StringProperty()

    # Statistics
    win = ndb.IntegerProperty(indexed=False)
    loss = ndb.IntegerProperty(indexed=False)
    # Average game length in minutes
    avg_game_duration = ndb.IntegerProperty(indexed=False)
