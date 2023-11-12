# imports for handling http
from urllib.parse import urlencode
# imports for environment variables
import os
from dotenv import load_dotenv
from flask import Flask, request
import webbrowser

# Load environment variables for client id and secret
load_dotenv()

client_id =  os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

callback_url = "http://localhost:3000/callback"
auth_url = "http://accounts.spotify.com/authorize?" 

# Setting headers for authenication request
auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": callback_url,
    "scope": "user-library-read"
}

webbrowser.open(auth_url + urlencode(auth_headers))

print("Starting app")
# Starting Flask app to listen to authenication response
app = Flask(__name__)

@app.route('/callback')
def callback():
    global auth_code
    auth_code = request.args.get("code") 
    print(auth_code)

    webbrowser.open("https://www.spotify.com",new=0)
    os._exit(0)
    return ""

if __name__ == '__main__':
    app.run(port=3000)


