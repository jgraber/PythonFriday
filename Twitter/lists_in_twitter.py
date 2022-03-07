import tweepy
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

# create a new list
list_name = "News created with Tweepy"
description='News about Python'
list = api.create_list(name=list_name,
                       mode='private',
                       description=description)
print(f"New list id: {list.id}: {list.name} [{list.member_count}]")
print("-" * 50)

# add a single account to a list
result = api.add_list_member(list_id=list.id,screen_name='pythonbytes')
print(f"Current members: {result.member_count}")

# add accounts to a list
accounts = ['PythonNewsread', 'PythonWeekly']
result = api.add_list_members(list_id=list.id, screen_name=accounts)
print(f"Current members: {result.member_count}")

print("-" * 50)

# remove an account from a list
result = api.remove_list_member(list_id=list.id,screen_name='pythonbytes')
print(f"Current members: {result.member_count}")

print("-" * 50)

# show all lists owned by a user (default: current user)
user_name = 'PythonFriday'
lists = api.get_lists(screen_name=user_name)
for entry in lists:
    print(f"{entry.id} - {entry.name} ({entry.mode}|{entry.member_count})")

print("-" * 50)

# show timeline of a list
list_id = 1500933128113770505
timeline = api.list_timeline(list_id=list_id,include_rts=False,count=3)

for tweet in timeline:
    print(f"{tweet.id} [{tweet.created_at}] (@{tweet.user.screen_name}):")
    print(f"{tweet.text}\n")

print(len(timeline))
print("-" * 50)

# remove a list
try:
    result = api.destroy_list(list_id=list.id)
    print(f"{result.id} removed")
except tweepy.errors.NotFound:
    print("list already removed")

print("-" * 50)
