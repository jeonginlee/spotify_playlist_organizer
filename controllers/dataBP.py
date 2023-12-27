from flask import Blueprint, redirect, url_for, render_template
import requests
import json
from models.database import SpotifyDB 
from models.data_handler import DataHandler

# Setting globals
db = SpotifyDB()
dataHandler = DataHandler()

spotify_url = "https://api.spotify.com/v1"      # leading url for spotify API

# Data endpoints --------------------------------------------------------------
dataBP = Blueprint('dataBP', __name__, template_folder="templates", url_prefix='/data')
@dataBP.route('/setToken/<auth_token>')
def setToken(auth_token):
    global token
    token = auth_token

    return redirect(url_for('dataBP.home'))

@dataBP.route('/home')
def home():
    return render_template('home.html')

@dataBP.route('/getPlaylists')
def getPlaylists():
    url = spotify_url + "/me/playlists?limit=50&offset=0"
    while(url):
        response = makeRequest(url)
        if response != None:
            for item in response["items"]:
                dataHandler.addPlaylist(item["id"], item["name"])
            url = response["next"]
        else:
            url = None

    print("Playlists loaded")
    return render_template('playlists.html', playlists=dataHandler.getPlaylists())

# Will get user liked songs if playlist query parameter is missing
@dataBP.route('/getTracks/<playlistId>')
def getTracks(playlistId):
    if playlistId != "User":
        print("searching for playlist " + playlistId)
        url = spotify_url + "/playlists/" + playlistId + "/tracks?limit=50&offset=0"
    else:
        url = spotify_url + "/me/tracks?limit=50&offset=0"
    while(url):
        response = makeRequest(url)
        if response != None:
            for item in response["items"]:
                track = item["track"]
                dataHandler.addTrack(track["id"], track["name"])
                dataHandler.addTrackArtists(track["id"], track["artists"])
            url = response["next"]
        else:
            url = None

    print("User tracks loaded")
    return redirect(url_for('dataBP.getArtistGenres'))

@dataBP.route('/getArtistGenres')
def getArtistGenres():
    url = spotify_url + '/artists'
    section = 1
    while(1):
        ids = dataHandler.getArtistIds(section)
        if ids == None: break # end of data

        response = makeRequest(url, ids)
        if response != None:
            # Add artist, genre and mapping to database
            for artist in response["artists"]:
                dataHandler.addArtistGenres(artist["id"], artist["genres"])
                db.insertArtists(artist["id"],artist["name"],artist["href"])
                for genre in artist["genres"]:
                    db.insertGenres(genre)
                    db.insertArtistToGenre(artist["name"],genre)

            section += 1
            break
        else:
            break

    print("Artist data loaded")
    return redirect(url_for('dataBP.getTrackData'))

@dataBP.route('/getTrackData')
def getTrackData():
    url = spotify_url + '/audio-features'
    section = 1
    while(1):
        ids = dataHandler.getTrackIds(section)
        if ids == None: break # end of data

        response = makeRequest(url, ids)
        if response != None: 
            for feature in response["audio_features"]:
                Id = feature["id"]
                track = dataHandler.getTrackObj(Id)

                db.insertTracks(
                    feature["acousticness"],
                    feature["analysis_url"],
                    feature["danceability"],
                    feature["duration_ms"],
                    feature["energy"],
                    Id,
                    feature["instrumentalness"],
                    feature["key"],
                    feature["liveness"],
                    feature["loudness"],
                    feature["mode"],
                    track.name,
                    feature["speechiness"],
                    feature["tempo"],
                    feature["time_signature"],
                    feature["track_href"],
                    feature["type"],
                    feature["uri"],
                    feature["valence"]
                )

                for genre in track.getGenres():
                    db.insertTrackToGenre(track.name, genre)

            section += 1
        else: 
            break
    print(str(dataHandler.getNumTracks()) + " songs loaded")
    return render_template("loaded.html", numTracks=dataHandler.getNumTracks())
# Helper functions --------------------------------------------------------

# Returns json data, None if request failed
def makeRequest(url, ids=None):
    headers = {
        "Authorization": "Bearer " + token
    }

    print("Making request to " + url)
    if ids == None: r = requests.get(url, headers=headers)
    else: 
        params = { "ids": ids }
        r = requests.get(url, params = params, headers=headers)

    if r.ok:
        return r.json()
    else:
        print("Request failed for url: " + url)
        print("\t" + json.dumps(r.json()))
        print("ids: " + ids)
        headers = {
            "Authorization": "Bearer " + token
        }
        headers = {
            "Authorization": "Bearer " + token
        }
        headers = {
            "Authorization": "Bearer " + token
        }
        return None


