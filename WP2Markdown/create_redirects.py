from usp.tree import sitemap_tree_for_homepage

pf186_old =  "2023/08/filter-data-in-your-pandas-dataframe/"
pf186_new = "https://pythonfriday.dev/2023/08/186-filter-data-in-pandas/"

tree = sitemap_tree_for_homepage('https://improveandrepeat.com/')

pages = []

for page in tree.all_pages():
    if "/python-friday-" in page.url and page.url not in pages:
        pages.append(page.url)


with open("redirects.txt", "w") as f:
    for page in pages:
        target = str(page)
        target = target.replace("improveandrepeat.com", "pythonfriday.dev")
        target = target.replace("/python-friday-", "/")
        source = str(page)
        source = source.replace("https://improveandrepeat.com/", "")
        f.write(f"RewriteRule ^{source}?$ {target} [QSD,R=302,L]\n")

    f.write(f"RewriteRule ^{pf186_old}?$ {pf186_new} [QSD,R=302,L]\n")

print("redirects written to redirects.txt")
# https://httpd.apache.org/docs/trunk/mod/mod_rewrite.html#rewriterule
# https://httpd.apache.org/docs/trunk/rewrite/flags.html#flag_qsd
# https://en.wikipedia.org/wiki/HTTP_302