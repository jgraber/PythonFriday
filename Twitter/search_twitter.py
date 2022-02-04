import tweepy
import os
from dotenv import load_dotenv
load_dotenv()


bearer_token = os.getenv('bearer-token')

client = tweepy.Client(bearer_token)

# Search Recent Tweets

# This endpoint/method returns Tweets from the last seven days

response = client.search_recent_tweets("#Python",expansions=("author_id"),user_fields="username,name")
# The method returns a Response object, a named tuple with data, includes,
# errors, and meta fields
print(response.meta)
users = {}

for user in response.includes['users']:
    # print(user.username)
    # print(user.name)
    users[user.id] = f"{user.name} (@{user.username})"
    print(users[user.id])
    # print(dir(inclu))

# In this case, the data field of the Response returned is a list of Tweet
# objects
tweets = response.data

# Each Tweet object has default id and text fields
for tweet in tweets:
    print('-' * 50)
    print(f"{tweet.id} - {users[tweet.author_id]}:\n {tweet.text} \n\n")
    # print(dir(tweet))