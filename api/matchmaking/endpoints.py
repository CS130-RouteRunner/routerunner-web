"""API endpoints for matchmaking purposes."""

import json
import webapp2
import logging
from pubnub import Pubnub
from models.lobby import Lobby
from models.user import User
from models.session import Session

from google.appengine.ext import ndb

PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"
REQ_USERS = 2   # Number of users needed to start a game

pubnub = Pubnub(publish_key=PUBLISH_KEY,
                subscribe_key=SUBSCRIBE_KEY, ssl_on=False, uuid="admin")


def callback(message, channel):
    print "Channel %s: (%s)" % (channel, message)


@ndb.transactional(xg=True, retries=3)
def update_users(winner, loser):
    """Updates the winner and loser's win-loss statistics."""
    winner.win += 1
    loser.lose += 1
    ndb.put_multi([winner, loser])


class NewUserHandler(webapp2.RequestHandler):
    """Handler for creating a new user."""

    def post(self):
        """ Store new user in database.
        Request
            uid - user_id
        """
        data = json.loads(self.request.body)
        response = {}

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing uid (User id)'
            return self.response.out.write(json.dumps(response))

        user = User.query(User.uuid == uid).get()
        if user is None:
            logging.info("New user (" + str(uid) + ") has joined RouteRunner.")
            user = User(uuid=uid, nickname=uid)
            user.put()


class NewLobbyHandler(webapp2.RequestHandler):
    """Handler for creating a new game lobby."""

    def post(self):
        """ User creates a lobby.
        Request
            uid - user_id
            lid - name of lobby
        """
        data = json.loads(self.request.body)
        response = {}

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing uid (User id)'
            return self.response.out.write(json.dumps(response))
        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing lid (Lobby id)'
            return self.response.out.write(json.dumps(response))

        user = User.query(User.uuid == uid).get()
        # New User
        if user is None:
            logging.info("New user (" + str(uid) +
                         ") has joined RouteRunner.")
            user = User(uuid=uid, nickname=uid)
            user.put()
        # TODO: Make sure this user is actually who we think it is

        lobby = Lobby(lobby_id=lobby_id, users=[uid])
        # Check if this lobby already exists
        exists = Lobby.query(Lobby.lobby_id == lobby_id).get()
        if exists is None:
            lobby.put()

        response['status'] = 'success'
        self.response.out.write(json.dumps(response))


class JoinLobbyHandler(webapp2.RequestHandler):
    """Handler for joining an existing game lobby."""

    def get(self):
        """ Returns a list of available lobbies.
        Response
            lobbies - list of lobbies
        """
        q = Lobby.query(Lobby.started == False)
        lobbies = [lobby.lobby_id for lobby in q.iter()]
        response = {'status': 'success', 'data': {'lobbies': lobbies}}

        self.response.out.write(json.dumps(response))

    def post(self):
        """ User joins an existing lobby.
        Request:
            uid - user_id
            lid - lobby to join
        """
        data = json.loads(self.request.body)
        response = {}

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing uid (User id)'
            return self.response.out.write(json.dumps(response))

        q = User.query(User.uuid == uid)
        if q is None:
            logging.error("Non-existent user (" + str(uid) +
                          ") attempted to join lobby.")
        # TODO: Make sure this user is actually who we think it is

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing lid (Lobby id)'
            return self.response.out.write(json.dumps(response))

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()
        # Stale lobby
        if lobby is None:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = "Lobby " + lobby_id + " does not exist!"
            return self.response.out.write(json.dumps(response))

        # Lobby already has REQ_USERS in it
        if len(lobby.users) == REQ_USERS or lobby.started is True:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = "Lobby " + lobby_id + " is at max capacity!"
            return self.response.out.write(json.dumps(response))

        lobby.users.append(uid)
        lobby.started = True
        lobby.put()

        response['status'] = 'success'
        self.response.out.write(json.dumps(response))


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
        response = {}

        try:
            uid = data['uid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing uid (User id)'
            return self.response.out.write(json.dumps(response))

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing lid (Lobby id)'
            return self.response.out.write(json.dumps(response))

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
        if len(lobby.ready) == REQ_USERS:
            # TODO: Add logic for creating a Session here
            session = Session(channel_id=lobby_id, target_gold_amount="100",
                              user_ids=[])
            for i in range(len(lobby.ready)):
                session.user_ids.append(lobby.ready[i])
            session.put()
            response['type'] = "info"
            response['data'] = {"ready": "true"}
            pubnub.subscribe(lobby_id, callback)
            pubnub.publish(lobby_id, response)
            pubnub.unsubscribe(lobby_id)

            self.response.out.write(json.dumps(response))
        else:
            response['type'] = "info"
            response['data'] = {"ready": "false"}
            pubnub.subscribe(lobby_id, callback)
            pubnub.publish(lobby_id, callback)
            pubnub.unsubscribe(lobby_id)
            self.response.out.write(json.dumps(response))


class EndGameHandler(webapp2.RequestHandler):
    """Handler for ending a game."""

    def post(self):
        """ End game.
        Request
            uid - user id of user leaving
            lid - the game lobby to end
            sessid - the game session to end
            winner - user id of the winner
            loser - user id of the loser
        """
        data = json.loads(self.request.body)
        response = {}
        winner = None
        loser = None

        try:
            user_id = data['uid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing uid (User id)'
            return self.response.out.write(json.dumps(response))

        try:
            lobby_id = data['lid']
        except KeyError:
            self.error(400)
            response['status'] = 'error'
            response['msg'] = 'Missing lid (Lobby id)'
            return self.response.out.write(json.dumps(response))

        if 'winner' in data:
            winner = data['winner']
        else:
            loser = data['loser']

        # try:
        #     winner = data['winner']
        #     loser = data['loser']
        # except KeyError:
        #     self.error(400)
        #     response['status'] = 'error'
        #     response[
        #         'msg'] = 'Missing winner (id of winner) or loser (id of loser)'
        #     return self.response.out.write(json.dumps(response))

        # try:
        #     session_id = data['sessid']
        # except KeyError:
        #     self.error(400)
        #     failure_msg = {'error': 'Missing sessid (Game Session id)'}
        #     return self.response.out.write(json.dumps(failure_msg))

        lobby = Lobby.query(Lobby.lobby_id == lobby_id).get()

        # Lobby has not yet been deleted
        if lobby:
            # If there is only 1 user left, just delete lobby
            if len(lobby.users) == 1:
                if winner is not None:
                    win_user = User.query(User.uuid == winner).get()
                    win_user.win += 1
                    win_user.put()
                else:
                    lose_user = User.query(User.uuid == loser).get()
                    lose_user.loss += 1
                    lose_user.put()
                lobby.key.delete()
            # Otherwise, remove the user from lobby
            # Update the user's statistics
            else:
                lobby.users.remove(user_id)
                lobby.put()
                if winner is not None:
                    win_user = User.query(User.uuid == winner).get()
                    win_user.win += 1
                    win_user.put()
                else:
                    lose_user = User.query(User.uuid == loser).get()
                    lose_user.loss += 1
                    lose_user.put()

        # TODO: Session cleanup

        response['status'] = 'success'
        self.response.out.write(json.dumps(response))


routes = [
    ('/api/user/new', NewUserHandler),
    ('/api/matchmaking/new', NewLobbyHandler),
    ('/api/matchmaking/join', JoinLobbyHandler),
    ('/api/matchmaking/start', StartGameHandler),
    ('/api/matchmaking/end', EndGameHandler)
]
