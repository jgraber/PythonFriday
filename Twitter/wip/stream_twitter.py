import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv('api-key')
consumer_secret = os.getenv('api-key-secret')
access_token = os.getenv('access-token')
access_token_secret = os.getenv('access-token-secret')

# Subclass tweepy.Stream to print the tweets
class TweetPrinter(tweepy.Stream):

    def on_status(self, status):
        print('-'*50)
        print(f"{status.id} {status.user.name} (@{status.user.screen_name}) at {status.created_at} {status.text}")

# Initialize instance of the subclass
printer = TweetPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)

# Filter realtime Tweets by keyword
printer.filter(track=["#Python"])