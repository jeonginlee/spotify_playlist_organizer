from flask import Flask, request, redirect

# for browser control and making requests
import webbrowser
import requests
from urllib.parse import urlencode
import base64
import json

# controlling process and loading environment vars
import os
from dotenv import load_dotenv

from create_database import SpotifyDB

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

@app.route('/callback')
def callback():
    global auth_code
    auth_code = request.args.get("code") 
    print(auth_code)

    return redirect("/token")

@app.route('/token')
def get_token():
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

    return redirect('/get_user_tracks')

@app.route('/get_user_tracks')
def get_user_tracks():
    global tracks
    
    url = spotify_url+"/me/tracks?limit=50&offset=0"

    # Populate list of track ids
    tracks = []
    while(url):
        print("Making request to " + url + " for user tracks")
        r = requests.get(url,headers=headers)
        if(r.ok):
            js = r.json()
            for item in js["items"]:
                track = (item["track"]["id"], item["track"]["name"])
                tracks.append(track)

            url = js["next"]
            #url = None #XXX
        else:
            url = None

    return redirect('/get_track_data')

@app.route('/get_track_data')
def get_track_data():
    # connect to database
    db = SpotifyDB()

    # API only accepts max 100 tracks at a time
    start = 0
    end = 100
    size = len(tracks)
    while(start < size):
        url =spotify_url + "/audio-features"
        ids = ""
        track_ids = []
        track_data = {} # dictionary to keep track of name

        for track in tracks[start:end]:
            track_ids.append(track[0]) 
            track_data[track[0]] = track[1]

        params = {
            "ids": ",".join(track_ids)
        }

        print("Making request to " + url + " for track data")
        r = requests.get(url, params = params, headers=headers)

        if(r.ok): 
            js = r.json()
            for feature in js["audio_features"]:
                track_id = feature["id"]
                print("adding: "+ track_id + " : name: " + track_data[track_id])

                # Add to database!
                db.insert_track(
                    feature["acousticness"],
                    feature["analysis_url"],
                    feature["danceability"],
                    feature["duration_ms"],
                    feature["energy"],
                    track_id,
                    feature["instrumentalness"],
                    feature["key"],
                    feature["liveness"],
                    feature["loudness"],
                    feature["mode"],
                    track_data[track_id],
                    feature["speechiness"],
                    feature["tempo"],
                    feature["time_signature"],
                    feature["track_href"],
                    feature["type"],
                    feature["uri"],
                    feature["valence"]
                )

            start = end
            end += 100
        else: 
            start = size

    return str(len(tracks))

# XXX USED FOR TESTING
@app.route('/cleanup')
def cleanup():
    db = SpotifyDB()
    db.cleanup()
    return "Database cleaned up"

@app.route('/shutdown')
def shutdown():
    os._exit(0)
    return ""

print("running")
if __name__ == '__main__':
    app.run(port=3000)
    print("flask response deployed")
