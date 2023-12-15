import numpy as np
import sys
sys.path.insert(0, "../models")
sys.path.insert(0, "../")

# Necessary for piping output to file 
sys.stdout.reconfigure(encoding='utf-8')

from database import SpotifyDB
from data_handler import DataHandler

db = SpotifyDB()
data = DataHandler()

def getSimilarity():
    trackData = db.getTrackData()
    tracks = {}
    for track in trackData:
        # Unpacking all data for readability
        (acousticness,analysis_url,danceability,duration_ms,energy,
        Id,instrumentalness,music_key,liveness,loudness,mode,name,
        speechiness,tempo,time_signature,track_href,TYPE,uri,valence) = track

        data.addTrack(Id, name)
        data.addTrackData(acousticness,analysis_url,danceability,duration_ms,energy,
            Id,instrumentalness,music_key,liveness,loudness,mode,
            speechiness,tempo,time_signature,track_href,TYPE,uri,valence)
        
        # Convert to array and map it
        tracks[Id] = np.array([danceability, energy, valence])


    # testing with track "If you love me" since R&B should be easy to find
    # similar songs for
    targetId = "0BTGqPIW9acmhhUmENkq5r" 
    normTarget = np.linalg.norm(tracks[targetId])
    simScores = {}
    for testId in tracks:
        normTest = np.linalg.norm(tracks[testId]) 
        cosSim = np.dot(tracks[targetId], tracks[testId]) / (normTarget*normTest)
        simScores[cosSim] = testId
        print(data.getTrackName(testId))
        print(tracks[targetId])
        print(tracks[testId])
        print("Num: " + str(np.dot(tracks[targetId], tracks[testId])))
        print("Den: " + str((normTarget*normTest)))
        print("Sim: " + str(cosSim))
        print('\n')

    sortedScores = sorted(simScores.keys())
    for score in sortedScores:
        print(f"Name: {data.getTrackName(simScores[score])}")
        print(f"\tScore: {score}")


if __name__ == "__main__":
    getSimilarity()
