from model.model import Track, Artist

class DataHandler(object):
    def __init__(self):
        self.tracks = {}
        self.artists = {}

    # Takes in a track object from spotify API response to keep track of 
    #    added tracks and their artsists
    def addTrack(self, trackObj):
        track = Track(trackObj["id"], trackObj["name"], trackObj["artists"])
        self.tracks[track.Id] = track

        for artist in track.artists:
            self.artists[artist.Id] = artist

    # Comma deliminated string of track Ids in the 100 track section
    #   Sections are 1 indexed, returns None if beyond size of track array
    def getTrackIds(self, section):  
        start = (section-1)*100
        size = len(self.tracks)
        if start >= size:
            return None

        trackIds = list(self.tracks.keys())[start:start+100]
        return ",".join(trackIds)

    # Returns Track object by Id
    def getTrackObj(self, Id):
        return self.tracks[Id]

    # Updates Artist object with genre info 
    def addArtistGenres(self, artistId, genres):
        if self.artists[artistId] != None:
            self.artists[artistId].addGenres(genres)

    # Returns a comma deliminated string of artist Ids in the 50 artist section
    #   Sections are 1 indexed, returns None if beyond size of track array
    def getArtistIds(self, section):
        start = (section-1)*50
        size = len(self.artists)
        if start >= size:
            return None
        
        artistIds = list(self.artists.keys())[start:start+50]
        return ",".join(artistIds)

    
