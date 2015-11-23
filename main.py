"""
Main endpoint for GAE app.

Creates the master app and the url routes.
"""

import webapp2

from api import map
from api import matchmaking
from api import communication
from api import stats


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello world!')

routes = [
    ('/', MainHandler),
]

routes += map.routes
routes += matchmaking.routes
routes += communication.routes
routes += stats.routes

app = webapp2.WSGIApplication(routes, debug=True)
