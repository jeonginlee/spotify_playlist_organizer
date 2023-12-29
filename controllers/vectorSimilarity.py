import numpy as np
import sys
from extensions import *

# Necessary for piping output to file 
sys.stdout.reconfigure(encoding='utf-8')

def loadTrackData():
    trackData = db.getTrackData()
    tracks = {}
    for track in trackData:
        # Unpacking all data for readability
        (acousticness,analysis_url,danceability,duration_ms,energy,
        Id,instrumentalness,music_key,liveness,loudness,mode,name,
        speechiness,tempo,time_signature,track_href,TYPE,uri,valence) = track

        dataHandler.addTrack(Id, name)
        dataHandler.addTrackData(acousticness,analysis_url,danceability,duration_ms,energy,
            Id,instrumentalness,music_key,liveness,loudness,mode,
            speechiness,tempo,time_signature,track_href,TYPE,uri,valence)
        
        # Convert to array and map it
        tracks[Id] = np.array([danceability, energy, valence])
    
    return tracks

def cosineSim(tracks, targetId):
    normTarget = np.linalg.norm(tracks[targetId])
    simScores = []
    for testId in tracks:
        normTest = np.linalg.norm(tracks[testId]) 
        cosSim = np.dot(tracks[targetId], tracks[testId]) / (normTarget*normTest)
        simScores.append((cosSim, testId))

    # Reversing to store higher matches ahead in list
    return sorted(simScores, reverse=True, key=lambda item: item[0])


def euclideanDist(tracks, targetId):
    target = tracks[targetId] 
    distances = []
    for testId in tracks:
        dist = np.linalg.norm(target - tracks[testId])
        distances.append((dist, testId))
   
    return sorted(distances, key=lambda item: item[0])

if __name__ == "__main__":
    sys.path.insert(0, "../models")
    sys.path.insert(0, "../")

    from database import SpotifyDB
    from data_handler import DataHandler

    db = SpotifyDB()
    dataHandler = DataHandler()

    import argparse

    parser = argparse.ArgumentParser()
    helpText = '''
        Method used to calculate similarity score.
        'e' for Euclidean distance 
        'c' for cosine similarity
    '''
    parser.add_argument('--method', '-m', default='c', help=helpText, required=True)
    args = parser.parse_args()

    targetId = "5qW6ZYct54PhKliCntyxRX" # cover me up jason isbell
    tracks = loadTrackData()

    if args.method == 'c':
        scores = cosineSim(tracks, targetId) 
    elif args.method == 'e':
        scores = euclideanDist(tracks, targetId)
    else: 
        raise Exception("Calculation method not specified.")
    
    # Print scores
    for score in scores:
        print(f"Name: {dataHandler.getTrackName(score[1])}")
        print(f"\tScore: {score[0]}")

        

