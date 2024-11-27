from usp.tree import sitemap_tree_for_homepage
import requests
import time

pages_original = []

pf186 =  "https://improveandrepeat.com/2023/08/filter-data-in-your-pandas-dataframe/"
tree = sitemap_tree_for_homepage('https://improveandrepeat.com/')

for page in tree.all_pages():
    if "/python-friday-" in page.url and page.url not in pages_original:
        pages_original.append(page.url)

pages_original.append(pf186)

print("\n" * 10)
print(f"pages to check: {len(pages_original)}")

for page in pages_original:
    time.sleep(1)
    r = requests.get(page)
    if r.history:
        old = r.history[0]
        print(f"{r.status_code} - {old.is_redirect} - {old.url} => {r.url}")
    else:
        print(f"{r.status_code} - False - {r.url}")
