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

api = tweepy.API(auth, wait_on_rate_limit=True)

# user = api.get_user(screen_name='j_graber')
# print(user.screen_name)
# print(user.followers_count)
# print(user.friends_count)
# for friend in user.friends():
#    print(friend.screen_name)

# print("----------------------")

# for page in tweepy.Cursor(api.get_followers, screen_name="j_graber",
#                           count=100).pages(10):
#     # print(len(page))
#     # print(dir(page))
#     # pp.pprint(page)
#     for user in page:
#         print(f"{user.id} - {user.name} (@{user.screen_name}): P:{user.protected}, {user.following}, {user.followers_count}, {user.friends_count}")


# print("----------------------")
# for page in tweepy.Cursor(api.get_friends, screen_name="j_graber",
#                           count=100).pages(10):
#     for user in page:
#         print(f"{user.id} - {user.name} (@{user.screen_name}): P:{user.protected}, {user.followers_count}, {user.friends_count}, {user.created_at}, {user.statuses_count}")

# for follower in tweepy.Cursor(api.get_followers, count=1000).items():
#     print(follower.screen_name)
#default_profile_image

followers = []
friends = []

print("----------------------")
print(f"Followers (peoply who follow {screen_name})")
for page in tweepy.Cursor(api.get_followers, screen_name=screen_name,
                          count=100).pages(10):
    for user in page:
        name = f"{user.id} - {user.name} (@{user.screen_name})"
        followers.append(name)
print(f"Followers: {len(followers)}")

print("----------------------")
print(f"Friends (peoply {screen_name} follows)")
for page in tweepy.Cursor(api.get_friends, screen_name=screen_name,
                          count=100).pages(10):
    for user in page:
        name = f"{user.id} - {user.name} (@{user.screen_name})"
        friends.append(name)
print(f"Friends: {len(friends)}")

friends_who_not_follow_back = np.setdiff1d(friends,followers)

with open(f"not_follow_back_{screen_name}.txt", "w") as f:
    for people in friends_who_not_follow_back:
        print(people)
        f.write(f"{people}\n")

print(f"Friends not Followers: {len(friends_who_not_follow_back)}")