from flask import Blueprint, redirect, url_for, request
from urllib.parse import urlencode
import base64

import requests
import json

import os
from dotenv import load_dotenv

# Setting globals
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
callback_url = "http://localhost:3000/authorize/callback"
auth_url = "http://accounts.spotify.com/authorize?" 
token_url = "https://accounts.spotify.com/api/token"

# Authorize endpoints -------------------------------------------------------
authorize = Blueprint('authorize', __name__, template_folder="templates", url_prefix='/authorize')
@authorize.route('/')
def start():
    scope = "user-library-read playlist-read-private"
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": callback_url,
        "scope": scope
    }
    return redirect(auth_url + urlencode(auth_headers))

@authorize.route('/callback')
def callback():
    return redirect(url_for('authorize.getToken', auth_code=request.args.get("code")))

@authorize.route('/token/<auth_code>')
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

        print("Token retrieved: " + token)

    return redirect(url_for('dataBP.setToken', auth_token=token))


