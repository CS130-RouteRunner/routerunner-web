import webapp2
import unittest
import webtest
import json
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from api import matchmaking
import util_test
import collections


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

    def testNewLobbyHandler(self):
        """Tests lobby creation handler."""
        endpoint = '/api/matchmaking/new'

        response = self.testapp.post_json(endpoint, {}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing uid (User id)')

        response = self.testapp.post_json(
            endpoint, {'uid': 'cs130'}, expect_errors=True)
        body = json.loads(response.body)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(body['status'], 'error')
        self.assertEqual(body['msg'], 'Missing lid (Lobby id)')
