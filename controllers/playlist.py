from flask import Blueprint, redirect, url_for, render_template
from extensions import *

playlist = Blueprint('playlist', __name__, template_folder="templates", url_prefix='/playlist')

@playlist.route('/')
def home():
    return render_template('playlistCreation.html')

@playlist.route('/listTracks')
def listTracks():
    return render_template('listTracks.html', tracks=dataHandler.getTrackNames())
