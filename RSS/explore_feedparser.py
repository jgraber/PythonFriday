from datetime import datetime
from time import mktime
import feedparser

f = feedparser.parse('https://improveandrepeat.com/category/pythonfriday/feed/')

print("Title: " + f.feed.title)
print("Site: " + f.feed.link)
print("Generator: " + f.feed.generator)
print("Last updated: " +f.feed.updated)

for post in f.entries:
    dt = datetime.fromtimestamp(mktime(post.published_parsed)).strftime("%Y-%m-%d")
    print(f"{post.title} ({dt})")
    # print(f"{post.title} ({post.published}) - {post.link}")
    # print(post.summary)
    # for key in post.keys():
    #     print(key)

