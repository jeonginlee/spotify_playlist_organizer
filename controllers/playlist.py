from flask import Blueprint, redirect, url_for, render_template
from extensions import *

from controllers.vectorSimilarity import loadTrackData, euclideanDist

playlist = Blueprint('playlist', __name__, template_folder="templates", url_prefix='/playlist')

@playlist.route('/')
def home():
    return render_template('playlistCreation.html')

@playlist.route('/listTracks')
def listTracks():
    print(dataHandler.getNumTracks())
    return render_template('listTracks.html', tracks=dataHandler.getTracks())

@playlist.route('/generatePlaylist/<targetId>')
def generatePlaylist(targetId):
    trackData = loadTrackData()
    scores = euclideanDist(trackData, targetId)

    tracks = [] 

    for score in scores[0:25]:
        tracks.append(dataHandler.getTrackName(score[1]))

    # XXX Print scores for testing 
    for score in scores:
        print(f"Name: {dataHandler.getTrackName(score[1])}")
        print(f"\tScore: {score[0]}")

    return render_template('playlist.html', tracks=tracks)
