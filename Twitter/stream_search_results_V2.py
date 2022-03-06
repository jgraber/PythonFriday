import tweepy
from tweepy import StreamingClient, StreamRule
import os
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.getenv('bearer-token')

class TweetPrinterV2(tweepy.StreamingClient):
    
    def on_tweet(self, tweet):
        print(f"{tweet.id} {tweet.created_at} ({tweet.author_id})): {tweet.text}")
        print("-"*50)

printer = TweetPrinterV2(bearer_token)

# clean-up pre-existing rules
rule_ids = []
result = printer.get_rules()
for rule in result.data:
    print(f"rule marked to delete: {rule.id} - {rule.value}")
    rule_ids.append(rule.id)

if(len(rule_ids) > 0):
    printer.delete_rules(rule_ids)
    printer = TweetPrinterV2(bearer_token)
else:
    print("no rules to delete")

# add new rules    
# rule = StreamRule(value="Python")
rule = StreamRule(value="NumPy")
printer.add_rules(rule)

printer.filter(expansions="author_id",tweet_fields="created_at")