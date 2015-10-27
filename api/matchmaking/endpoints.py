import json
import webapp2
from pubnub import Pubnub
from models.lobby import Lobby

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
        pubnub = Pubnub(publish_key=PUBLISH_KEY,
                        subscribe_key=SUBSCRIBE_KEY, ssl_on=False)
        data = json.loads(self.request.body)
        channel_id = pubnub.uuid    # Change this to data['uid'] later
        print channel_id
        pubnub.publish(LOBBY_PREFIX + channel_id, CREATION_MSG)
        response = {'lobby-id': channel_id}
        lobby = Lobby(id=channel_id, users=[channel_id])
        lobby.put()
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
            lobbies.append(lobby.key.id())

        lobbies.append("hi")
        self.response.out.write(json.dumps(lobbies))

    def post(self):
        """ User subscribes to a channel.
        Request:
            uid - user_id
            cid - channel to join
        """
        pubnub = Pubnub(publish_key=PUBLISH_KEY,
                        subscribe_key=SUBSCRIBE_KEY, ssl_on=False)
        data = json.loads(self.request.body)
        user_id = pubnub.uuid   # Change this to data['uid'] later
        channel_id = data['cid']
        pubnub.subscribe(channel_id, callback)
        pubnub.publish(channel_id, user_id + " has joined the lobby.")
        lobby = Lobby.get_by_id(channel_id)
        lobby.users.append(user_id)


class StartGameHandler(webapp2.RequestHandler):
    """Web handler for starting a game."""

    def post(self):
        """ Start game by both users.
        Request
            uid - user_id
            cid - channel the game is located in
        """
        pubnub = Pubnub(publish_key=PUBLISH_KEY,
                        subscribe_key=SUBSCRIBE_KEY, ssl_on=False)
        data = json.loads(self.request.body)
        user_id = data['uid']
        channel_id = data['cid']
        pubnub.publish(channel_id, "Game is about to begin.")


routes = [
    ('/api/matchmaking/new', NewLobbyHandler),
    ('/api/matchmaking/join', JoinLobbyHandler),
    ('/api/matchmaking/start', StartGameHandler)
]
