"""Utility functions for testing."""

from google.appengine.ext import ndb
from models.lobby import Lobby
from models.user import User


def create_lobby(lid, started=False):
    """Creates a lobby with lid that has the user lid in it."""
    lobby = Lobby(lobby_id=lid, users=[lid], started=started)
    lobby.put()


def create_lobbies(lid_list, started=False):
    """Creates a list of lobbies."""
    lobby_list = [Lobby(lobby_id=name, users=[name], started=started)
                  for name in lid_list]
    ndb.put_multi(lobby_list)


def create_user(uid):
    """Creates a user."""
    user = User(uuid=uid, nickname=uid)
    user.put()


def create_users(uid_list):
    """Creates a list of users."""
    user_list = [User(uuid=uid, nickname=uid) for uid in uid_list]
    ndb.put_multi(user_list)
