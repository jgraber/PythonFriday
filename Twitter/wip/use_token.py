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
user_access_token = os.getenv('access-token')
user_access_token_secret = os.getenv('access-token-secret')

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(user_access_token,user_access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


user = api.get_user(screen_name='j_graber')
print(user.screen_name)
print(user.followers_count)
print(user.friends_count)