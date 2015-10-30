import json
import webapp2
from pubnub import Pubnub
from models.route import Route
from models.session import Session
from models.user_session import UserSession
from google.appengine.api import users
from google.appengine.ext import ndb


PUBLISH_KEY = "pub-c-7fd0bf0a-96ef-42eb-8378-a52012ac326a"
SUBSCRIBE_KEY = "sub-c-a5a6fc48-79cc-11e5-9720-0619f8945a4f"


def callback(message, channel):
    """
    :param message: String to print
    :param channel: Channel we're in
    """
    print "Channel %s: (%s)" % (channel, message)


class ClientToServerHandler(webapp2.RequestHandler):
    """Handler for the client to server communication."""

    def post(self):
        """ User sends gold and route info to server.
        Request
            uid - user_id
            cid - channel_id
            data - message
        """
        data = json.loads(self.request.body)
        uid = data['uid']
        print uid
        cid = data['cid']
        print cid
        ucg = data['current_gold']
        print "The user's current gold is " + ucg
        r = data['route']
        print "The route is: " + r

        pointsList = r.split(";")
        ndb.GeoPoint()
        rid = uid + "-" + cid
        route = Route(route_id=rid, list_of_points=[])
        for i in range(len(pointsList)):
            lng = pointsList[i].split()[0]
            lat = pointsList[i].split()[1]
            route.list_of_points.append(ndb.GeoPoint(lng, lat))
        route.put()
        usid = uid + "-" + cid
        user_session = UserSession(user_session_id=usid, base_point="", drop_off_point="", user_current_gold=ucg, route_id=rid)
        user_session.put()
        # session = Session.query(Session.channel_id == cid).get()
        pubnub = Pubnub(publish_key=PUBLISH_KEY,
                             subscribe_key=SUBSCRIBE_KEY, ssl_on=False, uuid=str(uid))
        pubnub.subscribe(cid, callback)
        pubnub.publish(cid, uid + " has selected a route")
        response = {'user-session-id': usid}
        self.response.out.write(json.dumps(response))

class ServerToClientHandler(webapp2.RequestHandler):
    """Handler for the client to server communication."""
    def get(self):
        """ Returns a list of available lobbies.
        """
        data = json.loads(self.request.body)
        cid = data["cid"]
        session = Session.query(Session.channel_id == cid).get()
        target_gold_amount = session.target_gold_amount
        print target_gold_amount
        response = {'target_gold_amount': target_gold_amount}
        self.response.out.write(json.dumps(response))


routes = [
    ('/api/matchmaking/init', ClientToServerHandler)
]
