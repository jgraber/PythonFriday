import tweepy
from tweepy import StreamingClient, StreamRule
import os
from dotenv import load_dotenv
load_dotenv()


bearer_token = os.getenv('bearer-token')

rule = StreamRule(value="Python")

# client = StreamingClient(bearer_token)
# # client.add_rules(rule)
# client.filter()

class IDPrinter(tweepy.StreamingClient):
    users = {}

    def on_tweet(self, tweet):
        None
        # print(dir(tweet))
        # print(tweet)
        # exit()
        # print(self.includes)
        # print("-"*50)
        # print(f"{tweet.id} {tweet.created_at} ({tweet.author_id})): {tweet.text}")
        # # print(f"{tweet.id} {tweet.created_at} ({tweet.user.username})): {tweet.text}")
        # print("-"*50)

    def on_includes(self, includes):
        print(includes)
        # print(dir(includes))
        # for user in includes['users']:
        #     self.users[user.id] = user
        #     print(self.users[user.id].username)
        #     # print(f"got user {user.screen_name}")
        # return super().on_includes(includes)

        

printer = IDPrinter(bearer_token)
result = printer.get_rules()
try:
    # clean-up pre-existing rules
    rules = result.data
    rule_ids = []
    for rule in rules:
        print(f"rule marked to delete: {rule.id} - {rule.value}")
        rule_ids.append(rule.id)

    printer.delete_rules(rule_ids)

    if(len(rule_ids) > 0):
        printer = IDPrinter(bearer_token)

except Exception:
    print("Nothing to clear")

print("add new rules...")
printer.add_rules(rule)

print("Current rules:")
result = printer.get_rules()
rules = result.data
for rule in rules:
        print(f"rule: {rule.id} - {rule.value} - {rule.tag}")

print("ready to filter the Twitter stream")
printer.filter(tweet_fields="created_at,public_metrics,attachments",
        expansions="author_id,attachments.media_keys",
        user_fields="username,name,profile_image_url")
