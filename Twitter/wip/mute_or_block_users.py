import tweepy
import os
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
user_to_mute = "BILD"
response = client.get_user(username=user_to_mute)
user = response.data
print(f"id of user '@{user_to_mute}': {user.id}")

print("-" * 50)

# mute a user
result = client.mute(target_user_id=user.id)
print(f"user muted? {result.data['muting']}")

print("-" * 50)

# get a list of all muted users
muted = []
for response in tweepy.Paginator(client.get_muted, 
                                max_results=1000, 
                                limit=10):
    for user in response.data:
        muted.append(f"@{user.username} - {user.name} - {user.id}")

print("Muted users:")
for entry in muted:
    print(entry)

print("-" * 50)

# unmute a user
result = client.unmute(target_user_id=user.id)
print(f"user muted? {result.data['muting']}")

print("-" * 50)

# block a user
result = client.block(target_user_id=user.id)
print(f"user blocked? {result.data['blocking']}")

print("-" * 50)

# get a list of all blocked users
blocked = []
for response in tweepy.Paginator(client.get_blocked, 
                                max_results=1000, 
                                limit=10):
    for user in response.data:
        blocked.append(f"@{user.username} - {user.name} - {user.id}")

print("Blocked users:")
for entry in blocked:
    print(entry)

print("-" * 50)

# unblock a user
result = client.unblock(target_user_id=user.id)
print(f"user blocked? {result.data['blocking']}")

print("-" * 50)
