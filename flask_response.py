# imports for handling http
from urllib.parse import urlencode
import base64
from flask import Flask, request, redirect
import webbrowser
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
  
callback_url = "http://localhost:3000/callback"
auth_url = "http://accounts.spotify.com/authorize?" 
token_url = "https://accounts.spotify.com/api/token"

# Starting Flask app to listen to authenication response
app = Flask(__name__)

@app.route('/token')
def get_token():
    global token
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
        print("token: "+ token)

    return redirect("https://www.spotify.com")

@app.route('/callback')
def callback():
    # no error handling written yet!
    global auth_code
    auth_code = request.args.get("code") 
    print(auth_code)

    return redirect("/token")

@app.route('/shutdown')
def shutdown():
    os._exit(0)
    return ""

print("runnig")
app.run(port=3000)
print("ran")
