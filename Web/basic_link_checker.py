import requests
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage
from typing import NamedTuple


class Page(NamedTuple):
    url: str
    text: str


def read_sitemap(domain):
    tree = sitemap_tree_for_homepage(domain)
    pages = [page.url for page in tree.all_pages()]
    return pages


def find_links(pages):
    all_links = {}

    for page in pages:
        content = requests.get(page)
        soup = BeautifulSoup(content.text, "html.parser")
        links = soup.find_all("a")

        for link in links:
            if link.get("href").startswith("#"):
                continue

            if  link.get("rel") is not None and "nofollow" in link.get("rel"):
                continue

            link_text = link.get_text().strip()
            link_target = link.get("href")
            source = Page(page, link_text)

            if not link_target.lower().startswith("http"):
                link_target = page + link_target

            if link_target in all_links:
                all_links[link_target].append(source)
            else:
                all_links[link_target] = [source]
                
    return all_links


def check_links(all_links):
    status = {}

    for key in all_links:
        try:
            print(f"working on {key}")
            page = requests.head(key, timeout=5)
            code = page.status_code
        except ConnectionRefusedError:
            code = "ConnectionRefusedError"
        except Exception:
            code = "Exception"

        if code in status:
            status[code].append(key)
        else:
            status[code] = [key]

    return status


def create_report(all_links, result):
    with open("report_link_status.txt", "w", encoding="utf-8") as f:
        for code in result:
            f.write(f"- {code}\n")
            for page in result[code]:
                f.write(f"\t - {page}\n")
                for source in all_links[page]:
                    f.write(f"\t\t - {source.url} [{source.text}]\n")


if __name__ == "__main__":
    pages = read_sitemap("https://requests.readthedocs.io/")
    all_links = find_links(pages)
    result = check_links(all_links)
    create_report(all_links, result)
    