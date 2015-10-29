"""API endpoints for matchmaking purposes."""

import json
import webapp2
import logging
from pubnub import Pubnub
from models.lobby import Lobby
from models.user import User

PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"
LOBBY_PREFIX = "routerunner-"
GLOBAL_LOBBY = LOBBY_PREFIX + "global"
CREATION_MSG = "Creating new lobby."
START_GAME_MSG = "Game is about to begin."


class NewLobbyHandler(webapp2.RequestHandler):
    """Handler for creating a new game lobby."""

    def post(self):
        """ User creates a lobby.
        Request
            uid - user_id
        Response
            lid - name of lobby
        """
        data = json.loads(self.request.body)
        uid = data['uid']
        user = User.query(User.uuid == uid).get()
        # New User
        if user is None:
            logging.info("New user (" + str(uid) +
                         ") has joined Route Runner.")
            user = User(uuid=uid, nickname=uid)
            user.put()
        # TODO: Make sure this user is actually who we think it is

        lobby_id = LOBBY_PREFIX + uid
        lobby = Lobby(lobby_id=lobby_id, users=[uid])
        lobby.put()
        response = {'lid': lobby_id}

        self.response.out.write(json.dumps(response))


class JoinLobbyHandler(webapp2.RequestHandler):
    """Handler for joining an existing game lobby."""

    def get(self):
        """ Returns a list of available lobbies.
        Response
            lobbies - list of lobbies
        """
        q = Lobby.query()
        lobbies = [lobby.lobby_id for lobby in q.iter()]
        response = {'lobbies': lobbies}

        self.response.out.write(json.dumps(response))

    def post(self):
        """ User joins an existing lobby.
        Request:
            uid - user_id
            lid - lobby to join
        """
        data = json.loads(self.request.body)
        uid = data['uid']
        q = User.query(User.uuid == uid)
        if q is None:
            logging.error("Non-existent user (" + str(uid) +
                          ") attempted to join lobby.")
        # TODO: Make sure this user is actually who we think it is
        lobby_id = data['lid']

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()
        lobby.users.append(uid)
        lobby.put()


class StartGameHandler(webapp2.RequestHandler):
    """Handler for starting a game."""

    def post(self):
        """ Start game by both users.
        Request
            uid - user_id
            lid - the game lobby both users are playing in
        Response
        """
        data = json.loads(self.request.body)
        user_id = data['uid']
        channel_id = data['lid']

        # TODO: Add logic for creating Session


routes = [
    ('/api/matchmaking/new', NewLobbyHandler),
    ('/api/matchmaking/join', JoinLobbyHandler),
    ('/api/matchmaking/start', StartGameHandler)
]
