import requests
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
from typing import NamedTuple

class Page(NamedTuple):
    url: str
    text: str
    link_to: str


def read_sitemap(domain):
    tree = sitemap_tree_for_homepage(domain)
    pages = []

    for page in tree.all_pages():
        pages.append(page.url)
    
    return pages


def find_links(pages):
    all_links = []

    for page in pages:
        content = requests.get(page)
        soup = BeautifulSoup(content.text, 'html.parser')
        links = soup.find_all("a")

        for link in links:
            if link.get('href') == "#":
                continue

            if  link.get('rel') is not None and 'nofollow' in link.get('rel'):
                continue

            link_text = link.get_text().strip()
            link_target = link.get('href')

            if not link_target.lower().startswith("http"):
                link_target = page + link_target

            all_links.append(Page(page, link_text, link_target))
    
    return all_links


