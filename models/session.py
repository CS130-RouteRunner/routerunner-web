"""
Session model.
"""

from google.appengine.ext import ndb


class Session(ndb.Model):
    """Model that represents a single game."""
    channel_id = ndb.StringProperty()
    target_gold_amount = ndb.StringProperty()
    user_ids = ndb.StringProperty(repeated=True, indexed=False)