import json
import webapp2
from pubnub import Pubnub

PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"


def callback(message, channel):
    """
    :param message: String to print
    :param channel: Channel we're in
    """
    print "Channel %s: (%s)" % (channel, message)

pubnub = Pubnub(publish_key=PUBLISH_KEY,
                subscribe_key=SUBSCRIBE_KEY, ssl_on=False)
pubnub.subscribe("routerunner-lobby", callback)


class MatchmakingHandler(webapp2.RequestHandler):
    """Web handler for the game lobby/matchmaking."""

    def get(self):
        print "Connecting"
        pubnub.publish('routerunner-lobby', "HEllo World")


routes = [
    ('/api/matchmaking', MatchmakingHandler)
]
