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

import logging

logging.basicConfig(level=logging.DEBUG)

# use user authentication tokens
# auth = tweepy.OAuthHandler(api_key, api_secret)
# auth.set_access_token(user_token,user_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key, consumer_secret=api_secret,
    access_token=user_token, access_token_secret=user_token_secret,
    wait_on_rate_limit=True
)

# # show all lists owned by a user (default: current user)
# lists = api.get_lists() # .get_lists(screen_name='j_graber')
# for li in lists:
#     print(f"{li.id} - {li.name} ({li.mode}) - [{li.member_count}]")

# print("-" * 50)

# # show timeline of a list
# list_id = 1498823450231771137
# timeline = api.list_timeline(list_id=list_id)

# for s in timeline:
#     print(f"{s.id} [{s.created_at}] (@{s.user.screen_name}):")
#     print(f"{s.text}\n")

# print("-" * 50)

# create a new list
list_name = "People_I_Follow_20220304c"
description='People I followed that day'
# list = api.create_list(name=list_name,
#                        mode='private',
#                        description='People I followed that day')
# print(f"New list id: {list.id}: {list.name}")

result = client.create_list(name=list_name, description=description, private=True, user_auth=True)
# print(result)
list_id = result.data['id']

print("-" * 50)

# add people to list

# ret = client.create_list(name="abc", private=True)
# print(ret)
# print(ret.data["id"])
print("-" * 50)

# ret = client.add_list_member(id='1499488896454909956',user_id='58932896',user_auth=True)
# print(ret)

print("-" * 50)
screen_name = "PythonFriday"
# for page in tweepy.Cursor(api.get_friends, screen_name=screen_name,
#                           count=100).pages(10):
#     batch = []
#     for user in page:
#         print(".")
#         ret = batch.append(str(user.id))
#         client.add_list_member(id=list.id, user_id=user.id, user_auth=True)
#         print(ret)
#     separator = ','
#     batch_users = separator.join(batch)
#     print(len(batch))
#     print(batch_users)
# for page in tweepy.Cursor(client.get_users_following, screen_name=screen_name,
#                           count=100).pages(10):
#     for user in page:
#         print(f"{user.id} {user.screen_name}")
friends = 0
for response in tweepy.Paginator(client.get_users_following, id=58932896,
                                    max_results=1000, limit=5):
    # print(response.meta)
    # print(response)
    for user in response.data:
        print(user.id)
        client.add_list_member(id=list_id,user_id=user.id,user_auth=True)
        friends += 1
    print(f"added {friends} members to list")
    # len(response.data)
    # for user in response.data:
    #     print(user.id)
    # ret = api.add_list_members(list_id=list.id, user_id=batch_users)
    # print(ret)