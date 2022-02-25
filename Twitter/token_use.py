import tweepy
import random
import os
from dotenv import load_dotenv
load_dotenv()

# read keys from .env
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')
user_token = os.getenv('access-token')
user_token_secret = os.getenv('access-token-secret')

# use user authentication tokens
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(user_token,user_token_secret)
api = tweepy.API(auth)

# Create a tweet - random() to not write same tweet twice
api.update_status(f"Another Tweet with #Tweepy! {random.random()}")

print("Tweeted with your stored credentials")