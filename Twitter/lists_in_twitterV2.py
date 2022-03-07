import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# read keys from .env
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')
user_token = os.getenv('access-token')
user_token_secret = os.getenv('access-token-secret')
bearer_token = os.getenv('bearer-token')

# use user authentication tokens
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key, consumer_secret=api_secret,
    access_token=user_token, access_token_secret=user_token_secret,
    wait_on_rate_limit=True
)

# create a new list
list_name = "News created with Tweepy"
description='News about Python'
response = client.create_list(name=list_name,
                        private=True,
                        description=description)
list = response.data
list_id = response.data['id']
print(f"New list id: {list_id}: {response.data['name']}")
print("-" * 50)

# add a single account to a list
id_pythonbytes = 793685808645451776
response = client.add_list_member(id=list_id,
                                  user_id=id_pythonbytes)
print(f"Add member succeeded: {response.data['is_member']}")

# add accounts to a list
id_PythonNewsread = 886608290712629248
accounts = ['PythonNewsread', 'PythonWeekly']
response = client.add_list_member(id=list_id,
                                  user_id=id_PythonNewsread)
print(f"Add member succeeded: {response.data['is_member']}")

id_PythonWeekly = 373620985
response = client.add_list_member(id=list_id,
                                  user_id=id_PythonWeekly)
print(f"Add member succeeded: {response.data['is_member']}")

print("-" * 50)

# remove an account from a list
response = client.remove_list_member(id=list_id,
                                  user_id=id_pythonbytes)
print(f"Add still member: {response.data['is_member']}")

print("-" * 50)

# show all lists owned by a user (default: current user)
id_PythonFriday = 1492915170166943745
response = client.get_owned_lists(id=id_PythonFriday)
lists = response.data
for entry in lists:
    print(f"{entry.id} - {entry.name} (Private: {entry.private}|{entry.member_count})")

print("-" * 50)

# show timeline of a list
show_list_id = 1500933128113770505
# timeline = api.list_timeline(list_id=show_list_id,include_rts=False,count=3)
response = client.get_list_tweets(id=show_list_id,
                                    max_results=3,
                                    user_fields="username,name",
                                    expansions="author_id")
users = {user.id : user for user in response.includes['users']}

timeline = response.data
print(timeline)
for tweet in timeline:
    print(f"{tweet.id} [{tweet.created_at}] (@{users[tweet.author_id]}):")
    print(f"{tweet.text}\n")

print(len(timeline))
print("-" * 50)

# remove a list
try:
    response = client.delete_list(id=list_id)
    print(f"List deleted: {response.data['deleted']}")
except tweepy.errors.NotFound:
    print("list already removed")

print("-" * 50)
