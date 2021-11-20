from datetime import datetime
from time import mktime
import feedparser

d = feedparser.parse('https://improveandrepeat.com/category/pythonfriday/feed/')

print("Title: " + d.feed.title)
print("Site: " + d.feed.link)
print("Generator: " + d.feed.generator)
print("Last updated: " +d.feed.updated)

for post in d.entries:
    # dt = datetime.fromtimestamp(mktime(post.published_parsed)).strftime("%Y-%m-%d")
    # print(f"{post.title} ({dt}) - {post.link}")
    print(f"{post.title} ({post.published}) - {post.link}")
    print(post.summary)
    # for key in post.keys():
    #     print(key)

