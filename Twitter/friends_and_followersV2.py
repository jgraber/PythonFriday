import tweepy
import random
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# read keys from .env
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')
consumer_key = os.getenv('client-id')
consumer_secret = os.getenv('client-secret')
user_token = os.getenv('access-token')
user_token_secret = os.getenv('access-token-secret')
bearer_token = os.getenv('bearer-token')

# use user authentication tokens
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(user_token,user_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token=bearer_token,
    access_token=user_token, access_token_secret=user_token_secret,
    wait_on_rate_limit=True
)


# list friends
friends = []
screen_name = 'j_graber'
print(f"Friends (accounts {screen_name} follows)")
# for page in tweepy.Cursor(api.get_friends, screen_name=screen_name,
#                           count=200).pages(10):
#     for user in page:
#         name = f"{user.id} - {user.name} (@{user.screen_name})"
#         # print(name)
#         friends.append(name)
#     print(len(page))

friends = []
for response in tweepy.Paginator(client.get_users_following,
                                id=58932896,
                                max_results=1000, 
                                limit=10):
    for user in response.data:
        name = f"{user.id} - {user.name} (@{user.username})"
        friends.append(name)
    print(len(response.data))    
print(f"Friends: {len(friends)}")

print("-" * 50)

# list followers
followers = []
print(f"Followers (accounts who follow {screen_name})")
# for page in tweepy.Cursor(api.get_followers, screen_name=screen_name,
#                           count=200).pages(10):
#     for user in page:
#         name = f"{user.id} - {user.name} (@{user.screen_name})"
#         followers.append(name)
#     print(len(page))
for response in tweepy.Paginator(client.get_users_followers,
                                id=58932896,
                                max_results=1000, 
                                limit=10):
    for user in response.data:
        name = f"{user.id} - {user.name} (@{user.username})"
        followers.append(name)
    print(len(response.data))    
print(f"Followers: {len(followers)}")

print("-" * 50)

friends_who_not_follow_back = np.setdiff1d(friends,followers)

with open(f"not_follow_back_{screen_name}.txt", "w") as f:
    for people in friends_who_not_follow_back:
        f.write(f"{people}\n")

print(f"Friends but not Followers: {len(friends_who_not_follow_back)}")
