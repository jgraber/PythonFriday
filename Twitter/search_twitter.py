import tweepy
import os
from dotenv import load_dotenv
load_dotenv()


bearer_token = os.getenv('bearer-token')

client = tweepy.Client(bearer_token)

# Search Recent Tweets (last 7 days)
response = client.search_recent_tweets("#Python Friday 112",max_results=15)
tweets = response.data

for tweet in tweets:
    print('-' * 50)
    print(f"{tweet.id} ({tweet.created_at}) - {tweet.author_id}:\n {tweet.text} \n")

print("-" * 50)

# expanded search
response = client.search_recent_tweets(
                "#VisitOslo", 
                max_results=10,
                expansions="author_id,attachments.media_keys",
                tweet_fields="created_at,public_metrics,attachments",
                user_fields="username,name,profile_image_url",
                media_fields="public_metrics,url,height,width,alt_text")

# process users
users = {}
for user in response.includes['users']:
    # print(user.username)
    # print(user.name)
    users[user.id] = f"{user.name} (@{user.username}) [{user.profile_image_url}]"
    print(users[user.id])
    # print(dir(inclu))

# process media attachment
media = {}
for item in response.includes['media']:
    media[item.media_key] = f"{item.url} - {item.height}x{item.width} - Alt: {item.alt_text}"
    print(media[item.media_key])


tweets = response.data

# The expanded tweet offers a lot more data
for tweet in tweets:
    print('-' * 50)
    print(f"{tweet.id} ({tweet.created_at}) - {users[tweet.author_id]}:\n {tweet.text} \n")
    metric = tweet.public_metrics
    print(f"retweets: {metric['retweet_count']} | likes: {metric['like_count']}")
    if tweet.attachments is not None:
        for media_key in tweet.attachments['media_keys']:
            print(f"Media attachment: {media[media_key]}")
