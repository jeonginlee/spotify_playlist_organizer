from track import Track

class DataHandler(object):
    def __init__(self):
# XXX turn this into dict? can i still iterate through to create list for getTracksId
        self.tracks = []
        
        # XXX turn this into new Artist object
        self.artists = {}

    # Takes in a track object from spotify API response to keep track of 
    #    added tracks and their artsists
    def addTrack(self, trackObj):
        track = Track(trackObj["id"], trackObj["name"], trackObj["artists"])
        self.tracks.append(track)

        # XXX
        # will the Artist object that gets added here be shared between the
        # references? Track holds Artist, and it also lives here
        # if so, we can leave the references, and use the list of Artists to
        # generate query for spotify API to load genres for all Artists

        for artist in track.artists:
            self.artists[artist["id"]] = artist

    # Returns a tuple 
    #   First: comma deliminated string of track Ids in the 100 track section
    #   Second: map of ids to track name
    #   Sections are 1 indexed, returns None if beyond size of track array
    def getTrackIds(self, section):  
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
