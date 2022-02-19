import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# read keys from .env
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')

# prepare OAuthHandler
auth = tweepy.OAuthHandler(api_key, api_secret)
print(auth.get_authorization_url())

# Enter that PIN to continue
verifier = input("PIN (oauth_verifier= parameter): ")

# Complete authenthication
auth.get_access_token(verifier)

# store these tokens in .env file:
print(f"access-token={auth.access_token}")
print(f"access-token-secret={auth.access_token_secret}")