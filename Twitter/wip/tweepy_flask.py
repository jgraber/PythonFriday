import flask
from flask import redirect, request
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')

app = flask.Flask(__name__)


@app.route('/')
def index():
    auth = tweepy.OAuthHandler(api_key, api_secret)
    return redirect(auth.get_authorization_url())


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    args = request.args
    oauth_token = args['oauth_token']
    oauth_verifier = args['oauth_verifier']
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
    auth.get_access_token(oauth_verifier)
    
    user_tokens = f"access-token={auth.access_token}<br>access-token-secret={auth.access_token_secret}"
    return user_tokens
    

if(__name__ == "__main__"):
    app.run(port=6006)