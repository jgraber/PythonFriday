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
    # api_key = os.getenv('api-key')
    # api_secret = os.getenv('api-key-secret')
    auth = tweepy.OAuthHandler(api_key, api_secret)
    print(auth.request_token)
    return redirect(auth.get_authorization_url())

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    args = request.args
    print(args)
    oauth_token = args['oauth_token']
    print({'oauth_token': oauth_token })
    oauth_verifier = args['oauth_verifier']
    print(oauth_verifier)
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.request_token = {'oauth_token': oauth_token, 'oauth_token_secret': oauth_verifier}
    print("----")
    auth.get_access_token(oauth_verifier)
    # auth.set_request_token(oauth_token, oauth_verifier)

    user_tokens = f"access-token={auth.access_token}<br>access-token-secret={auth.access_token_secret}"
    # user_tokens = f"{oauth_verifier}<br>b"
    return user_tokens
    

if(__name__ == "__main__"):
    app.run(port=6006)