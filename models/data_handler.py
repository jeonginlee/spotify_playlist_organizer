from models.model import *

class DataHandler(object):
    def __init__(self):
        self.tracks = {}
        self.artists = {}
        self.playlists = {}

    # Takes in a track object from spotify API response to keep track of 
    #    added tracks and their artsists
    def addTrack(self, Id, name):
        self.tracks[Id] = Track(Id, name)

    # Adds artist data for each track
    def addTrackArtists(self, Id, artists):
        track = self.tracks[Id] 
        track.addArtists(artists)
        for artist in track.artists:
            self.artists[artist.Id] = artist

    def addTrackData(self,acousticness,analysis_url,danceability,duration_ms,energy,
                Id,instrumentalness,music_key,liveness,loudness,mode,
                speechiness,tempo,time_signature,track_href,TYPE,uri,valence):
        self.tracks[Id].addData(acousticness,analysis_url,danceability,duration_ms,energy,
                instrumentalness,music_key,liveness,loudness,mode,
                speechiness,tempo,time_signature,track_href,TYPE,uri,valence)

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

    def getTrackName(self, Id):
        return self.tracks[Id].name

    # Returns a list of track names for display
    def getTrackNames(self):
        names = []
        for track in self.tracks.values():
            names.append(track.name)
        return names

    def getNumTracks(self):
        return len(self.tracks)

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

    def addPlaylist(self, Id, name):
        self.playlists[Id] = Playlist(Id, name)

    # Returns a list of playlist objects
    def getPlaylists(self):
        return self.playlists.values()
