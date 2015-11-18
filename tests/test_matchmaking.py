import webapp2
import unittest
import webtest
import json
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import collections

import util_test
from api import matchmaking
from models.user import User
from models.lobby import Lobby


class MatchmakingTest(unittest.TestCase):
    """Tests matchmaking."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a WSGI Application
        app = webapp2.WSGIApplication(matchmaking.routes)
        # Wrap app in WebTest's TestApp
        self.testapp = webtest.TestApp(app)
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

        self.lobby_names = ["glau", "julian", "patrick",
                            "rchen93", "xtrina", "kailin"]
        self.started = ["grace", "neerav"]
        util_test.create_lobbies(self.lobby_names)
        util_test.create_lobbies(self.started, True)
        self.full = ["kailin"]
        util_test.fill_lobbies(self.full)

    def tearDown(self):
        """Tear down test fixtures."""
        self.testbed.deactivate()

    def testJoinLobbyGetHandler(self):
        """Should only return lobbies that have not started."""
        response = self.testapp.get('/api/matchmaking/join')
        body = json.loads(response.body)
        response_lobbies = body['data']['lobbies']
        self.assertEqual(response.status_int, 200)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(len(response_lobbies), len(self.lobby_names))
        self.assertEqual(collections.Counter(response_lobbies),
                         collections.Counter(self.lobby_names))

    def testJoinLobbyPostHandler(self):
        """Tests lobby joining handler."""
        endpoint = '/api/matchmaking/join'

        # No user id supplied
        response = self.testapp.post_json(endpoint, {}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing uid (User id)')

        # No lobby id supplied
        response = self.testapp.post_json(
            endpoint, {'uid': 'cs130'}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing lid (Lobby id)')

        # Lobby does not exist anymore
        response = self.testapp.post_json(
            endpoint, {'uid': 'cs130', 'lid': 'routerunner'}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Lobby routerunner does not exist!')

        # Lobby is full
        request = {'uid': 'cs130', 'lid': self.full[0]}
        response = self.testapp.post_json(
            endpoint, request, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Lobby ' +
                         self.full[0] + ' is at max capacity!')

        # Successfully joined lobby
        request = {'uid': 'cs130', 'lid': 'rchen93'}
        response = self.testapp.post_json(endpoint, request)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(body['status'], 'success')
        lobby = Lobby.query(Lobby.lobby_id == 'rchen93').get()
        self.assertEqual(len(lobby.users), 2)
        self.assertEqual(collections.Counter(lobby.users),
                         collections.Counter(['rchen93', 'cs130']))

    def testNewLobbyHandler(self):
        """Tests lobby creation handler."""
        endpoint = '/api/matchmaking/new'

        # No user id supplied
        response = self.testapp.post_json(endpoint, {}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing uid (User id)')

        # No lobby id supplied
        response = self.testapp.post_json(
            endpoint, {'uid': 'cs130'}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing lid (Lobby id)')

        # Test that a new User is created if we've never seen this user before
        uid = 'routerunner'
        lid = 'cs130'
        request = {'uid': uid, 'lid': lid}
        user = User.query(User.uuid == uid).get()
        lobby = Lobby.query(Lobby.lobby_id == lid).get()
        self.assertIsNone(user)
        self.assertIsNone(lobby)

        response = self.testapp.post_json(endpoint, request)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(body['status'], 'success')
        user = User.query(User.uuid == uid).get()
        lobby = Lobby.query(Lobby.lobby_id == lid).get()
        self.assertIsNotNone(user)
        self.assertIsNotNone(lobby)
