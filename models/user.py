"""
User model.
"""
from google.appengine.ext import ndb


class User(ndb.Model):
    """Model that represents a single User."""
    # Unique id for pubnub
    uuid = ndb.StringProperty()
    nickname = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    # Statistics
    win = ndb.IntegerProperty(indexed=False, default=0)
    loss = ndb.IntegerProperty(indexed=False, default=0)
    # Average game length in minutes
    avg_game_duration = ndb.IntegerProperty(indexed=False)
