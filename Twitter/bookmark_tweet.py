import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# read keys from .env
access_token_pkce = os.getenv('access-token-pkce')

client = tweepy.Client(access_token_pkce)

python_release = "1536895050176667649"
photo_tweet = "1416838512117231627"

# add tweet to bookmarks
response = client.bookmark(tweet_id=python_release)
print(f"Tweet {python_release} bookmarked: {response.data['bookmarked']}")
response = client.bookmark(tweet_id=photo_tweet)
print(f"Tweet {photo_tweet} bookmarked: {response.data['bookmarked']}")

print("-" * 50)

response = client.get_bookmarks(
    expansions="author_id,attachments.media_keys",
    tweet_fields="created_at,public_metrics,attachments",
    user_fields="username,name,profile_image_url",
    media_fields="public_metrics,url,height,width,alt_text")
# print(response)

tweets = response.data

# users = {}
# for user in response.includes['users']:
#     # print(user.username)
#     # print(user.name)
#     users[user.id] = f"{user.name} (@{user.username}) [{user.profile_image_url}]"
#     print(users[user.id])

# for tweet in tweets:
#     print(f"{tweet.id} ({tweet.created_at}) - {users[tweet.author_id]}:\n {tweet.text} \n")
users = {}
for user in response.includes['users']:
    users[user.id] = f"{user.name} (@{user.username}) [{user.profile_image_url}]"
    
# process media attachment
media = {}
if 'media' in response.includes:
    for item in response.includes['media']:
        media[item.media_key] = f"{item.url} - {item.height}x{item.width} - Alt: {item.alt_text}"
 
tweets = response.data
 
# The expanded tweet offers a lot more data
for tweet in tweets:
    print('-' * 50)
    print(f"{tweet.id} ({tweet.created_at}) - {users[tweet.author_id]}:\n {tweet.text} \n")
    metric = tweet.public_metrics
    print(f"retweets: {metric['retweet_count']} | likes: {metric['like_count']}")
    if tweet.attachments is not None:
        for media_key in tweet.attachments['media_keys']:
            print(f"Media attachment: #{media[media_key]}")

print("-" * 50)
# remove tweet from bookmarks
response = client.remove_bookmark(tweet_id=python_release)
print(f"Tweet {python_release} bookmarked: {response.data['bookmarked']}")

response = client.remove_bookmark(tweet_id=photo_tweet)
print(f"Tweet {photo_tweet} bookmarked: {response.data['bookmarked']}")
