import flask
from flask import redirect, request
import tweepy
import random
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
    

@app.route('/tweet')
def tweet():
    # You would read these values from the session
    user_token = os.getenv('access-token')
    user_token_secret = os.getenv('access-token-secret')

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(user_token,user_token_secret)
    api = tweepy.API(auth)

    # Create a tweet - random() to not write same tweet twice
    api.update_status(f"A Tweet from Flask - {random.random()}")

    return "Tweet send with Flask"


if(__name__ == "__main__"):
    app.run(port=6006)