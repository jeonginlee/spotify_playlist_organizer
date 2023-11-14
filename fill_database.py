# imports for handling http
from urllib.parse import urlencode
import base64
from flask import Flask, request, redirect
import webbrowser
import requests
# imports for environment variables
import os
#import flask_response

from dotenv import load_dotenv
# Load environment variables for client id and secret
load_dotenv()

client_id =  os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

callback_url = "http://localhost:3000/callback"
auth_url = "http://accounts.spotify.com/authorize?" 
token_url = "https://accounts.spotify.com/api/token"

# Setting headers for authenication request
auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": callback_url,
    "scope": "user-library-read"
}

print("test")
webbrowser.open(auth_url + urlencode(auth_headers))

print("Starting app")
if __name__ == '__main__':
    exec(open("flask_response.py").read())
    print("flask response deployed")


