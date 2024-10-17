from usp.tree import sitemap_tree_for_homepage

pf186 =  "https://improveandrepeat.com/2023/08/filter-data-in-your-pandas-dataframe/"

tree = sitemap_tree_for_homepage('https://improveandrepeat.com/')

with open("redirects.txt", "w") as f:
    for page in tree.all_pages():
        if "/python-friday-" in page.url:
            target = str(page.url)
            target = target.replace("improveandrepeat.com", "pythonfriday.dev")
            target = target.replace("/python-friday-", "/")
            source = str(page.url)
            source = source.replace("https://improveandrepeat.com/", "")
            f.write(f"RewriteRule ^{source}?$ {target} [QSD,R=302,L]\n")

    f.write(f"RewriteRule ^2023/08/filter-data-in-your-pandas-dataframe/?$ https://pythonfriday.dev/2023/08/186-filter-data-in-pandas/ [QSD,R=302,L]\n")

print("redirects written to redirects.txt")
# https://httpd.apache.org/docs/trunk/mod/mod_rewrite.html#rewriterule
# https://httpd.apache.org/docs/trunk/rewrite/flags.html#flag_qsd
# https://en.wikipedia.org/wiki/HTTP_302