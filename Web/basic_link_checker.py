import requests
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
from typing import NamedTuple

class Page(NamedTuple):
    url: str
    text: str