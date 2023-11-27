from flask import Flask, request, redirect, url_for

import requests
from urllib.parse import urlencode
import base64
import json

# controlling process and loading environment variables
import os
from dotenv import load_dotenv

from database import SpotifyDB
from data_handler import DataHandler
import objects

# Setting globals
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
  
callback_url = "http://localhost:3000/callback"
auth_url = "http://accounts.spotify.com/authorize?" 
token_url = "https://accounts.spotify.com/api/token"
spotify_url = "https://api.spotify.com/v1"      # leading url for spotify API

app = Flask(__name__)
db = SpotifyDB()
data = DataHandler()

# Authorization endpoints -----------------------------------------------------
@app.route('/')
def start():
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": callback_url,
        "scope": "user-library-read"
    }
    return redirect(auth_url + urlencode(auth_headers))

@app.route('/callback')
def callback():
    return redirect(url_for('getToken', auth_code=request.args.get("code")))

@app.route('/token/<auth_code>')
def getToken(auth_code):
    global token,refresh_token,headers
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8") 
    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
         "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": callback_url
    }

    r = requests.post(token_url, data=token_data, headers=token_headers)
    if r.ok:
        token = r.json()["access_token"]
        refresh_token = r.json()["refresh_token"]

        headers = {
            "Authorization": "Bearer " + token
        }
        print("Token retrieved: " + token)

    return redirect(url_for('getUserTracks'))

# Data endpoints --------------------------------------------------------------
@app.route('/getUserTracks')
def getUserTracks():
    url = spotify_url + "/me/tracks?limit=50&offset=0"
    while(url):
        response = makeRequest(url)
        if response != None:
            for item in response["items"]:
                data.addTrack(item["track"])
            url = response["next"]
            url = None
        else:
            url = None

    print("User tracks loaded")
    return redirect(url_for('getArtistGenres'))

@app.route('/getArtistGenres')
def getArtistGenres():
    url = spotify_url + '/artists'
    section = 1
    while(1):
        ids = data.getArtistIds(section)
        if ids == None: break # end of data

        response = makeRequest(url, ids)
        if response != None:
            # Add artist, genre and mapping to database
            for artist in response["artists"]:
                data.addArtistGenres(artist["id"], artist["genres"])
                db.insertArtist(artist["id"],artist["name"],artist["href"])
                for genre in artist["genres"]:
                    db.insertGenre(genre)
                    db.insertArtistToGenre(artist["name"],genre)

            section += 1
            break
        else:
            break

    print("Artist data loaded")
    return redirect(url_for('getTrackData'))

@app.route('/getTrackData')
def getTrackData():
    url = spotify_url + '/audio-features'
    section = 1
    while(1):
        ids = data.getTrackIds(section)
        if ids == None: break # end of data

        response = makeRequest(url, ids)
        if response != None: 
            for feature in response["audio_features"]:
                Id = feature["id"]
                track = data.getTrackObj(Id)

                db.insertTrack(
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
    print("Track data loaded")
    return "hi"
# Helper functions --------------------------------------------------------

# Returns json data, None if request failed
def makeRequest(url, ids=None):

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
        return None


# USED FOR TESTING ---------------------------------------------------------
@app.route('/cleanup')
def cleanup():
    db.cleanup()
    return "Database cleaned up"

@app.route('/shutdown')
def shutdown():
    os._exit(0)
    return ""

# Main deployment -------------------------------------------------------------
if __name__ == '__main__':
    print("Deploying Flask...")
    app.run(port=3000)
