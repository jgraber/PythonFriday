import tweepy
import os
from dotenv import load_dotenv
load_dotenv()
import pprint
pp = pprint.PrettyPrinter()
import json

consumer_key = os.getenv('client-id')
consumer_secret = os.getenv('client-secret')
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')

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

for page in tweepy.Cursor(api.get_followers, screen_name="j_graber",
                          count=100).pages(10):
    print(len(page))
    # print(dir(page))
    # pp.pprint(page)
    for user in page:
        print(f"{user.id} - {user.name} (@{user.screen_name}): P:{user.protected}, {user.following}, {user.followers_count}, {user.friends_count}")


# print("----------------------")
# for follower in tweepy.Cursor(api.get_followers, count=1000).items():
#     print(follower.screen_name)

