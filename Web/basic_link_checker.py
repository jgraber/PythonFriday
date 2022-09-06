import requests
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
from typing import NamedTuple

class Page(NamedTuple):
    url: str
    text: str


def read_sitemap(domain):
    tree = sitemap_tree_for_homepage(domain)
    pages = []

    for page in tree.all_pages():
        pages.append(page.url)
    
    return pages

