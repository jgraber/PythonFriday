from datetime import datetime
from time import mktime
import feedparser
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

f = feedparser.parse('https://localhost:7066')

print("Title: " + f.feed.title)
print("Site: " + f.feed.link)
#print("Last updated: " +f.feed.updated)

for post in reversed(f.entries):
    #print(dir(post))
    print(f"{post.title} ({post.update}) - {post.link}")
    print(post.summary)
    for key in post.keys():
        print(key)

