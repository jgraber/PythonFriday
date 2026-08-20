import ebooklib
from ebooklib import epub


book = epub.read_epub("holmes_books\his_last_bow.epub")

print(book.get_metadata("DC", "title"))
# Output: [('His last bow', {})]

print("*" * 50)

print(book.get_metadata("DC", "creator"))
# Output: [('Arthur Conan Doyle', {'id': 'author_0'})]

print("*" * 50)

def print_toc(items, depth=0):
    for item in items:
        if isinstance(item, tuple):
            section, children = item
            print("  " * depth + section.title)
            print_toc(children, depth + 1)
        else:
            print("  " * depth + f"{item.title} -> {item.href}")

print_toc(book.toc)
# Output:
# His Last Bow -> 8617134549485746331_2350-h-0.htm.xhtml#pgepubid00000
# Preface -> 8617134549485746331_2350-h-0.htm.xhtml#pgepubid00001
# Contents -> 8617134549485746331_2350-h-0.htm.xhtml#pgepubid00002
# The Adventure of Wisteria Lodge
#   1. The Singular Experience of Mr. John Scott Eccles -> 8617134549485746331_2350-h-1.htm.xhtml#pgepubid00004
#   2. The Tiger of San Pedro -> 8617134549485746331_2350-h-1.htm.xhtml#pgepubid00005
# The Adventure of the Bruce-Partington Plans -> 8617134549485746331_2350-h-2.htm.xhtml#pgepubid00006
# The Adventure of the Devil’s Foot -> 8617134549485746331_2350-h-3.htm.xhtml#pgepubid00007
# The Adventure of the Red Circle
#   PART I -> 8617134549485746331_2350-h-4.htm.xhtml#pgepubid00009
#   PART II -> 8617134549485746331_2350-h-5.htm.xhtml#pgepubid00010
# The Disappearance of Lady Frances Carfax -> 8617134549485746331_2350-h-6.htm.xhtml#pgepubid00011
# The Adventure of the Dying Detective -> 8617134549485746331_2350-h-7.htm.xhtml#pgepubid00012
# His Last Bow: The War Service of Sherlock Holmes -> 8617134549485746331_2350-h-8.htm.xhtml#pgepubid00013
# THE FULL PROJECT GUTENBERG™ LICENSE -> 8617134549485746331_2350-h-9.htm.xhtml#pg-footer-heading

print("*" * 50)

for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    print(item.get_name(), item.get_id())

# Output:
# 8617134549485746331_2350-h-0.htm.xhtml pg-header
# 8617134549485746331_2350-h-1.htm.xhtml item4
# 8617134549485746331_2350-h-2.htm.xhtml item5
# 8617134549485746331_2350-h-3.htm.xhtml item6
# 8617134549485746331_2350-h-4.htm.xhtml item7
# 8617134549485746331_2350-h-5.htm.xhtml item8
# 8617134549485746331_2350-h-6.htm.xhtml item9
# 8617134549485746331_2350-h-7.htm.xhtml item10
# 8617134549485746331_2350-h-8.htm.xhtml item11
# 8617134549485746331_2350-h-9.htm.xhtml pg-footer
# toc.xhtml ncx
# wrap0000.xhtml coverpage-wrapper


print("*" * 50)
for item_id, _ in book.spine:
    item = book.get_item_with_id(item_id)
    print(item.get_name())
# Output:
# wrap0000.xhtml
# 8617134549485746331_2350-h-0.htm.xhtml
# 8617134549485746331_2350-h-1.htm.xhtml
# 8617134549485746331_2350-h-2.htm.xhtml
# 8617134549485746331_2350-h-3.htm.xhtml
# 8617134549485746331_2350-h-4.htm.xhtml
# 8617134549485746331_2350-h-5.htm.xhtml
# 8617134549485746331_2350-h-6.htm.xhtml
# 8617134549485746331_2350-h-7.htm.xhtml
# 8617134549485746331_2350-h-8.htm.xhtml
# 8617134549485746331_2350-h-9.htm.xhtml

print("*" * 50)

chapter = book.get_item_with_href("8617134549485746331_2350-h-2.htm.xhtml")
print(chapter.get_content()[0:500])
# Output
# b'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">\n  <head/>\n  <body>\n    <div class="chapter" id="pgepubid00006">\n\n<h2><a id="chap02"/>The Adventure of the Bruce-Partington Plans</h2>\n\n<p>\nIn the third week of November, in the year 1895, a dense yellow fog settled\ndown upon London. From the Monday to the Thursday'

print("*" * 50)

chapter = book.get_item_with_href("8617134549485746331_2350-h-2.htm.xhtml")
print(chapter.get_body_content()[0:500])
# Output
# b'<body class="x-ebookmaker x-ebookmaker-3">\n  <div class="chapter" id="pgepubid00006">\n\n<h2><a id="chap02"/>The Adventure of the Bruce-Partington Plans</h2>\n\n<p>\nIn the third week of November, in the year 1895, a dense yellow fog settled\ndown upon London. From the Monday to the Thursday I doubt whether it was ever\npossible from our windows in Baker Street to see the loom of the opposite\nhouses. The first day Holmes had spent in cross-indexing his huge book of\nreferences. The second and third had '

print("*" * 50)

from bs4 import BeautifulSoup

chapter = book.get_item_with_href("8617134549485746331_2350-h-2.htm.xhtml")
soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
print(soup.get_text(" ", strip=True)[0:500])


print("*" * 50)