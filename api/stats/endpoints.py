"""API endpoints for retrieving statistics."""

import json
import webapp2
import logging
from models.user import User


class UserStatsHandler(webapp2.RequestHandler):
    """Handler for player statistics."""

    def get(self, user_id):

        user = User.query(User.uuid == user_id).get()
        response = {}

        if user:
            response['status'] = 'success'
            response['data'] = {'win': user.win, 'loss': user.loss}
            self.response.out.write(json.dumps(response))
        else:
            self.error(404)
            response['status'] = 'error'
            response['msg'] = 'User not found!'


routes = [
    ('/api/stats/user/<user_id:\d+>', UserStatsHandler)
]
