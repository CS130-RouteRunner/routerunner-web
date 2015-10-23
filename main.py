"""
Main endpoint for GAE app.

Creates the master app and the url routes.
"""

import webapp2

from api import map


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello world!')

routes = [
    ('/', MainHandler),
]

routes += map.routes

app = webapp2.WSGIApplication(routes, debug=True)
