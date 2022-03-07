import tweepy
import os
import random
from dotenv import load_dotenv
load_dotenv()


# read keys from .env
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')
client_id = os.getenv('client-id')
client_secret = os.getenv('client-secret')
user_token = os.getenv('access-token')
user_token_secret = os.getenv('access-token-secret')
bearer_token = os.getenv('bearer-token')

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key, consumer_secret=api_secret,
    access_token=user_token, access_token_secret=user_token_secret,
    wait_on_rate_limit=True
)

screen_name = "PythonFriday"

# find user id by username
user_to_follow = "ThePSF"
response = client.get_user(username=user_to_follow)
user = response.data
print(f"id of user '@{user_to_follow}': {user.id}")

print("-" * 50)

# follow a user
result = client.follow_user(target_user_id=user.id)
print(f"user followed? {result.data['following']}")

# get a list of all users PythonFriday is following
friends = []
for response in tweepy.Paginator(client.get_users_following,
                                id=1492915170166943745,
                                max_results=1000, 
                                limit=10):
    for user in response.data:
        friends.append(f"@{user.username} - {user.name} - {user.id}")

print("Friends:")
for entry in friends:
    print(entry)

# unfollow a user
result = client.unfollow_user(target_user_id=user.id)
print(f"user unfollowed? {result.data['following']}")

print("-" * 50)

# like a tweet
tweet_id = 1499822223338655756
result = client.like(tweet_id=tweet_id)
print(f"liked the tweet? {result.data['liked']}")

print("-" * 50)

# retweet a tweet
result = client.retweet(tweet_id=tweet_id)
print(f"retweeted the tweet? {result.data['retweeted']}")

# write a tweet
result = client.create_tweet(
                text=f"A tweet from the V2 client of #Tweepy {random.random()}",
                reply_settings='following')
print(result)
print(f"Tweet #{result.data['id']} created")