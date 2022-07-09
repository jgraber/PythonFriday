import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# read keys from .env
client_id = os.getenv('client-id')
client_secret = os.getenv('client-secret')

# prepare OAuth2Handler
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri="https://127.0.0.1:6006/callback",
    # minimal scope to work with bookmarks
    scope=["bookmark.read", "bookmark.write",
        "tweet.read","users.read"],
    client_secret=client_secret
)

print(oauth2_user_handler.get_authorization_url())

verifier = input("Enter whole callback URL: ")

access_token = oauth2_user_handler.fetch_token(
    verifier
)

# store these tokens in .env file:
print(f"\naccess-token-pkce={access_token['access_token']}")
