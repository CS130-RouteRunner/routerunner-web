import json
import webapp2

from models.song import Song


class SongHandler(webapp2.RequestHandler):
    """Web handler for Song models."""

    def get(self):
        """ Returns the requested song.
        Request:
            id - id of song

        Response:
            Requested song in JSON form
        """
        song_id = self.request.get('id')
        song = Song.get_by_id(song_id)
        self.response.out.write(song.to_json())

    def post(self):
        """ Adds a song to the DB.
        Request:
            title - Title of song
            artist - Artist of song
            duration - Duration of song (seconds)
            genre - Genre of song

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
    ('/api/song', SongHandler),
]
