import tweepy
import random
import numpy as np
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
api = tweepy.API(auth, wait_on_rate_limit=True)


# list friends
friends = []
screen_name = 'j_graber'
print(f"Friends (accounts {screen_name} follows)")
for page in tweepy.Cursor(api.get_friends, screen_name=screen_name,
                          count=200).pages(10):
    for user in page:
        name = f"{user.id} - {user.name} (@{user.screen_name})"
        # print(name)
        friends.append(name)
    print(len(page))
    
print(f"Friends: {len(friends)}")

print("-" * 50)

# list followers
followers = []
print(f"Followers (accounts who follow {screen_name})")
for page in tweepy.Cursor(api.get_followers, screen_name=screen_name,
                          count=200).pages(10):
    for user in page:
        name = f"{user.id} - {user.name} (@{user.screen_name})"
        followers.append(name)
    print(len(page))
    
print(f"Followers: {len(followers)}")

print("-" * 50)

friends_who_not_follow_back = np.setdiff1d(friends,followers)

with open(f"not_follow_back_{screen_name}.txt", "w") as f:
    for people in friends_who_not_follow_back:
        f.write(f"{people}\n")

print(f"Friends but not Followers: {len(friends_who_not_follow_back)}")


# tweepy.errors.TooManyRequests: 429 Too Many Requests
# 88 - Rate limit exceeded

# Rate limit reached. Sleeping for: 821