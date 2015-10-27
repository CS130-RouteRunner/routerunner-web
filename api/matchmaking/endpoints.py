import json
import webapp2
from pubnub import Pubnub
from models.lobby import Lobby
from models.user import User
from google.appengine.api import users

PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"
LOBBY_PREFIX = "routerunner-"
GLOBAL_LOBBY = LOBBY_PREFIX + "global"
CREATION_MSG = "Creating new lobby."
START_GAME_MSG = "Game is about to begin."


def callback(message, channel):
    """
    :param message: String to print
    :param channel: Channel we're in
    """
    print "Channel %s: (%s)" % (channel, message)


class NewLobbyHandler(webapp2.RequestHandler):
    """Web handler for creating a new game lobby."""

    def post(self):
        """ User creates a lobby.
        Request
            uid - user_id
        """
        data = json.loads(self.request.body)
        uid = data['uid']
        print uid
        user = User.query(User.uuid == uid).get()
        # New User (Hack for lack of authentication atm)
        if user is None:
            print "User does not exist"
            pubnub = Pubnub(publish_key=PUBLISH_KEY,
                            subscribe_key=SUBSCRIBE_KEY, ssl_on=False)
            user = User(google_id="1234", email="roger@cs130.com",
                        uuid=pubnub.uuid, nickname="roger")
            user.put()
        else:
            # Connect using the user's unique identifier
            pubnub = Pubnub(publish_key=PUBLISH_KEY,
                            subscribe_key=SUBSCRIBE_KEY, ssl_on=False, uuid=str(uid))
        channel_id = pubnub.uuid
        print channel_id
        pubnub.publish(LOBBY_PREFIX + channel_id, CREATION_MSG)
        lobby = Lobby(channel_id=channel_id, users=[channel_id])
        lobby.put()
        response = {'lobby-id': channel_id}
        self.response.out.write(json.dumps(response))


class JoinLobbyHandler(webapp2.RequestHandler):
    """Web handler for joining an existing game lobby."""

    def get(self):
        """ Returns a list of available lobbies.
        """
        q = Lobby.query()
        lobbies = []
        for lobby in q.iter():
            print lobby
            print lobby.key.id()
            lobbies.append(lobby.channel_id)

        self.response.out.write(json.dumps(lobbies))

    def post(self):
        """ User subscribes to a channel.
        Request:
            uid - user_id
            cid - channel to join
        """
        data = json.loads(self.request.body)
        uid = data['uid']
        print uid
        q = User.query(User.uuid == uid)
        if q is None:
            print "THIS SHOULDNT HAPPEN"
        else:
            # Connect using the user's unique identifier
            pubnub = Pubnub(publish_key=PUBLISH_KEY,
                            subscribe_key=SUBSCRIBE_KEY, ssl_on=False, uuid=str(uid))
        channel_id = data['cid']
        pubnub.subscribe(channel_id, callback)
        pubnub.publish(channel_id, uid + " has joined the lobby.")
        lobby = Lobby.query(Lobby.channel_id == channel_id).get()
        lobby.users.append(uid)
        lobby.put()


class StartGameHandler(webapp2.RequestHandler):
    """Web handler for starting a game."""

    def post(self):
        """ Start game by both users.
        Request
            uid - user_id
            cid - channel the game is located in
        """
        data = json.loads(self.request.body)
        user_id = data['uid']
        channel_id = data['cid']
        pubnub = Pubnub(publish_key=PUBLISH_KEY,
                        subscribe_key=SUBSCRIBE_KEY, ssl_on=False, uuid=user_id)
        pubnub.publish(channel_id, "Game is about to begin.")


routes = [
    ('/api/matchmaking/new', NewLobbyHandler),
    ('/api/matchmaking/join', JoinLobbyHandler),
    ('/api/matchmaking/start', StartGameHandler)
]
