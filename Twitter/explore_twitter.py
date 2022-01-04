import os
from dotenv import load_dotenv
load_dotenv()


consumer_key = os.getenv('client-id')
consumer_secret = os.getenv('client-secret')
api_key = os.getenv('api-key')
api_secret = os.getenv('api-key-secret')

from twython import Twython
twitter = Twython(api_key, api_secret, oauth_version=2)

ACCESS_TOKEN = twitter.obtain_access_token()
print(ACCESS_TOKEN)
twitter = Twython(api_key, access_token=ACCESS_TOKEN)

# results = twitter.search(q='python', result_type='popular')
# for result in results:
#     print(result['id_str'])
    
user_tweets = twitter.get_user_timeline(screen_name='j_graber',
                                        include_rts=True)
for tweet in user_tweets:
    tweet['text'] = Twython.html_for_tweet(tweet)
    print(tweet['text'])