import json
import webapp2
from google.appengine.api import urlfetch

MAPBOX_DIRECTION_API = "https://api.mapbox.com/v4/directions/"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicmNoZW45MyIsImEiOiJjaWcyeDZ1NzExZ3FidGxreHpiNG5neTV5In0.0ZjmL0S4tNln-Op6vQzuRQ"
MAPBOX_PROFILE = "mapbox.driving/"


class MapHandler(webapp2.RequestHandler):
    """Web handler for the map."""

    def get(self):
        """ Returns a route based on two pairs of (lng, lat) coordinates semi-colon delimited.
        Request:
            waypoints - lng1,lat1;lng2,lat2

        Response:
            GeoJSON line
        """
        waypoints = json.loads(self.request.get('waypoints'))
        url = MAPBOX_DIRECTION_API + MAPBOX_PROFILE + \
            waypoints['lng'] + ";" + waypoints['lat'] + \
            ".json?access_token=" + MAPBOX_ACCESS_TOKEN
        result = urlfetch.fetch(url)
        data = json.loads(result.content)
        self.response.out.write(json.dumps(data['routes'][0]['geometry']))

    def post(self):
        """ Adds a map to the DB.
        Request:
            title - Title of map
            artist - Artist of map
            duration - Duration of map (seconds)
            genre - Genre of map

        Response:
            Success or failure
        """
        data = json.loads(self.request.body)
        title = data['title']
        artist = data['artist']
        duration = data['duration']
        genre = data['genre']

        # Set id manually to ensure uniqueness in datastore??
        song = Song(title=title, artist=artist,
                    duration=duration, genre=genre, id=title)
        song.put()

routes = [
    ('/api/map', MapHandler),
]
