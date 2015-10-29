"""API endpoints for matchmaking purposes."""

import json
import webapp2
import logging
from pubnub import Pubnub
from models.lobby import Lobby
from models.user import User

# PubNub will now be handled on client side
# PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
# SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"
# LOBBY_PREFIX = "routerunner-"
# GLOBAL_LOBBY = LOBBY_PREFIX + "global"
REQ_USERS = 2   # Number of users needed to start a game


class NewLobbyHandler(webapp2.RequestHandler):
    """Handler for creating a new game lobby."""

    def post(self):
        """ User creates a lobby.
        Request
            uid - user_id
            lid - name of lobby
        """
        data = json.loads(self.request.body)

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing uid (User id)'}
            return self.response.out.write(json.dumps(failure_msg))
        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing lid (Lobby id)'}
            return self.response.out.write(json.dumps(failure_msg))

        user = User.query(User.uuid == uid).get()
        # New User
        if user is None:
            logging.info("New user (" + str(uid) +
                         ") has joined Route Runner.")
            user = User(uuid=uid, nickname=uid)
            user.put()
        # TODO: Make sure this user is actually who we think it is

        lobby = Lobby(lobby_id=lobby_id, users=[uid])
        lobby.put()

        success_msg = {'msg': 'Saved'}
        self.response.out.write(json.dumps(success_msg))


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

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing uid (User id)'}
            return self.response.out.write(json.dumps(failure_msg))

        q = User.query(User.uuid == uid)
        if q is None:
            logging.error("Non-existent user (" + str(uid) +
                          ") attempted to join lobby.")
        # TODO: Make sure this user is actually who we think it is

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing lid (Lobby id)'}
            return self.response.out.write(json.dumps(failure_msg))

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()
        lobby.users.append(uid)
        lobby.put()

        success_msg = {'msg': 'Saved'}
        self.response.out.write(json.dumps(success_msg))


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

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing uid (User id)'}
            return self.response.out.write(json.dumps(failure_msg))

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing lid (Lobby id)'}
            return self.response.out.write(json.dumps(failure_msg))

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()

        if lobby is None:
            logging.error(
                "User (" + str(uid) + ") attempted to join non-existent Lobby (" + str(lobby_id) + ").")
        else:
            ready = lobby.ready
            # This is a new user who is ready
            if uid not in ready:
                lobby.ready.append(uid)
                lobby.put()

        response = {}
        # The game is ready to be started
        # Greater than for internal tool purposes
        if len(lobby.ready) >= REQ_USERS:
            # TODO: Add logic for creating a Session here
            response['ready'] = "true"
            self.response.out.write(json.dumps(response))
        else:
            response['ready'] = "false"
            self.response.out.write(json.dumps(response))


class EndGameHandler(webapp2.RequestHandler):
    """Handler for ending a game."""

    def post(self):
        """ End game.
        Request
            lid - the game lobby to end
            sessid - the game session to end
        """
        data = json.loads(self.request.body)

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            failure_msg = {'msg': 'Missing lid (Lobby id)'}
            return self.response.out.write(json.dumps(failure_msg))

        # try:
        #     session_id = data['sessid']
        # except KeyError:
        #     self.error(400)
        #     failure_msg = {'error': 'Missing sessid (Game Session id)'}
        #     return self.response.out.write(json.dumps(failure_msg))

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()

        # Lobby has not yet been deleted
        if lobby:
            lobby.key.delete()

        # TODO: Session cleanup


routes = [
    ('/api/matchmaking/new', NewLobbyHandler),
    ('/api/matchmaking/join', JoinLobbyHandler),
    ('/api/matchmaking/start', StartGameHandler),
    ('/api/matchmaking/end', EndGameHandler)
]
