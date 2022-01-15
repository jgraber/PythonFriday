import tweepy
import os
from dotenv import load_dotenv
load_dotenv()
import pprint
pp = pprint.PrettyPrinter()
import json
import numpy as np

consumer_key = os.getenv('client-id')
consumer_secret = os.getenv('client-secret')
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')
screen_name = "j_graber"

auth = tweepy.OAuthHandler(api_key, api_secret)

# This prints a URL that can be used to authorize your app
# After granting access to the app, a PIN to complete the authorization process
# will be displayed


print(auth.get_authorization_url())
# Enter that PIN to continue
verifier = input("PIN (oauth_verifier): ")

auth.get_access_token(verifier)
# store these tokens! https://developer.twitter.com/en/docs/authentication/oauth-1-0a/obtaining-user-access-tokens
print(auth.access_token)
print(auth.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)