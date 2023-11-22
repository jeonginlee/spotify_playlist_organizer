
class Artist(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name
        self.genres = []

    def addGenres(self):
        for genre in genres:
            self.genres.append(genre)

class Track(object):
    def __init__(self, Id, name, artists):
        self.Id = Id
        self.name = name
        self.artists = []
        for artist in artists:
            self.artists.append(Artist(artist["id"], artist["name"]))
        
    def getGenres():
        genres = []
        for artist in self.artists:
            for genre in artist.genres:
                genres.append(genre)

        return genres
