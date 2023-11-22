from track import Track

class DataHandler(object):
    def __init__(self):
        self.tracks = []
        self.artists = {}

    # Takes in a track object from spotify API response to keep track of 
    #    added tracks and their artsists
    def addTrack(self, trackObj):
        track = Track(trackObj["id"], trackObj["name"], trackObj["artists"])
        self.tracks.append(track)

        for artist in track.artists:
            self.artists[artist.Id] = artist

    # Returns a comma deliminated string of artist Ids in the 50 artist section
    #   Sections are 1 indexed, returns None if beyond size of track array
    def getArtistInfo(self, section):
        start = (section-1)*50
        size = len(self.tracks)
        if start >= size:
            return None, None
        
        artistIds = list(self.artists.keys())[start:start+50]

        # XXX just realized that this function is called to get ids to get the
        # genre info. might not need to keep track of genre since its getting
        # loaded to the database immediately
       # artistGenres = {}
       # for Id in artistIds:
       #     artistGenres[Id] = self.artists[Id].genres

        return ",".join(artistIds)


    # Returns a tuple 
    #   First: comma deliminated string of track Ids in the 100 track section
    #   Second: map of ids to track name
    #   Sections are 1 indexed, returns None if beyond size of track array
    def getTrackInfo(self, section):  
        start = (section-1)*100
        size = len(self.tracks)
        if start >= size:
            return None, None

        track_ids = []
        track_names = {}
        for track in self.tracks[start:start+100]:
            track_ids.append(track.Id) 
            track_names[track.Id] = track.name
        
        return ",".join(track_ids), track_names

