"""
Main endpoint for GAE app.

Creates the master app and the url routes.
"""

import webapp2

from api import map
from api import matchmaking
from api import communication


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello world!')

routes = [
    ('/', MainHandler),
]

routes += map.routes
routes += matchmaking.routes
routes += communication.routes

app = webapp2.WSGIApplication(routes, debug=True)
