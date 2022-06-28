from typing import NamedTuple

class Link(NamedTuple):
    url: str
    text: str
    
home = Link("http://127.0.0.1/home", "Home")

print(f"url: {home.url}")
print(f"text: {home.text}")

print("*" * 20)

home.text = "new"