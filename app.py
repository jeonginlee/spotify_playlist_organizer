from flask import Flask, request, redirect, url_for

# for browser control and making requests
import webbrowser
import requests
from urllib.parse import urlencode
import base64
import json

# controlling process and loading environment vars
import os
from dotenv import load_dotenv

from database import SpotifyDB
from data_handler import DataHandler

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
  
callback_url = "http://localhost:3000/callback"
auth_url = "http://accounts.spotify.com/authorize?" 
token_url = "https://accounts.spotify.com/api/token"
spotify_url = "https://api.spotify.com/v1"      # leading url for spotify API

# Opening browser for user authorization
auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": callback_url,
    "scope": "user-library-read"
}

webbrowser.open(auth_url + urlencode(auth_headers))

# Starting Flask app to listen to authenication response
app = Flask(__name__)
db = SpotifyDB()
data = DataHandler()

@app.route('/callback')
def callback():
    return redirect(url_for('get_token', auth_code=request.args.get("code")))

@app.route('/token/<auth_code>')
def get_token(auth_code):
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

    return redirect(url_for('get_user_tracks'))

@app.route('/get_user_tracks')
def get_user_tracks():
    url = spotify_url+"/me/tracks?limit=50&offset=0"
    while(url):
        print("Making request to " + url + " for user tracks")
        r = requests.get(url,headers=headers)
        if(r.ok):
            js = r.json()
            for item in js["items"]:
                data.addTrack(item["track"])
            url = js["next"]
            url = None #XXX
        else:
            url = None

    return redirect(url_for('get_track_data'))

@app.route('/get_track_data')
def get_track_data():
    url = spotify_url + "/audio-features"
    section = 1
    while(1):
        ids,names = data.getTrackIds(section)
        if ids == None: break # end of data

        params = {
            "ids": ids
        }

        print("Making request to " + url + " for track data")
        r = requests.get(url, params = params, headers=headers)

        if(r.ok): 
            js = r.json()
            for feature in js["audio_features"]:
                Id = feature["id"]
                print("adding: "+ Id + " : name: " + names[Id])

                # need to know genres for each artist by now
                # should do this in between the end of get_user_tracks and here
                # might be easiest to query for this data from handler by Id 
                # to return name and list of genres

                # Add to database!
                db.insert_track(
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
                    names[Id],
                    feature["speechiness"],
                    feature["tempo"],
                    feature["time_signature"],
                    feature["track_href"],
                    feature["type"],
                    feature["uri"],
                    feature["valence"]
                )

            section += 1
            break;    #XXX
        else: 
            print("Request failed")
            break;
    return "hi"

# XXX USED FOR TESTING
@app.route('/cleanup')
def cleanup():
    db.cleanup()
    return "Database cleaned up"

@app.route('/shutdown')
def shutdown():
    os._exit(0)
    return ""

if __name__ == '__main__':
    print("Deploying Flask...")
    app.run(port=3000)
