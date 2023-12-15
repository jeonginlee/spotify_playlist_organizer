class Artist(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name
        self.genres = []

    def addGenres(self,genres):
        for genre in genres:
            self.genres.append(genre)

class Track(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name

    def addArtists(self, artists):
        self.artists = []
        for artist in artists:
            self.artists.append(Artist(artist["id"], artist["name"]))
   
    def addData(self,acousticness,analysis_url,danceability,duration_ms,energy,
                instrumentalness,music_key,liveness,loudness,mode,
                speechiness,tempo,time_signature,track_href,TYPE,uri,valence):
        self.acousticness = acousticness
        self.analysis_url = analysis_url
        self.danceability = danceability
        self.duration_ms = duration_ms
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.music_key = music_key
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.time_signature = time_signature
        self.track_href = track_href
        self.TYPE = TYPE
        self.uri = uri
        self.valence = valence
        
    def getGenres(self):
        genres = []
        for artist in self.artists:
            for genre in artist.genres:
                genres.append(genre)

        return genres

class Playlist(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name
