
class Artist(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name
        self.genres = []

    def addGenres(self.genres):
        for genre in genres:
            self.genres.append(genre)

class Track(object):
	def __init__(self, Id, name, artists):
		self.Id = Id
		self.name = name
		self.artists = []
        for artist  in artists:
            self.artists.append(Artist(artist["id"], artist["name"]))
