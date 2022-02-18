import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

consumer_key = os.getenv('api-key')
consumer_secret = os.getenv('api-key-secret')
access_token = os.getenv('access-token')
access_token_secret = os.getenv('access-token-secret')

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        print('-'*50)
        print(f"{status.id} {status.user.name} (@{status.user.screen_name}) at {status.created_at} {status.text}")
        # print(dir(status))

# Initialize instance of the subclass
printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)

# Filter realtime Tweets by keyword
printer.filter(track=["Python"])