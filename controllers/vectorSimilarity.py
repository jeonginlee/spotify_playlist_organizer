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

import argparse


def loadTrackData():
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
    
    return tracks

def euclideanDist(tracks, targetId):
    target = tracks[targetId] 
    distances = {}
    for testId in tracks:
        score = np.linalg.norm(target - tracks[testId])
        distances[score] = testId
    
    sortedDist = sorted(distances.keys())
    for dist in sortedDist:
        print(f"Name: {data.getTrackName(distances[dist])}")
        print(f"\tDist: {dist}")
    

def cosineSim(tracks, targetId):
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
        cosineSim(tracks, targetId) 
    elif args.method == 'e':
        euclideanDist(tracks, targetId)
    else:
        raise Exception("Invalid method chosen.")
