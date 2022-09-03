>>> from bs4 import BeautifulSoup
 
>>> html_doc = '<p><i><a href="abc">Hello'
>>> soup = BeautifulSoup(html_doc, 'html.parser')
 
>>> print(soup.prettify()) 
<p>
 <i>
  <a href="abc">
   Hello
  </a>
 </i>
</p>

>>> import requests
 
>>> r = requests.get('https://ImproveAndRepeat.com/') 
>>> soup = BeautifulSoup(r.text, 'html.parser')

>>> soup.title      
<title>Improve &amp; Repeat</title>
 
>>> soup.title.text                 
'Improve & Repeat'

>>> soup.head       
<head>
<meta charset="utf-8"/>
<link href="https://gmpg.org/xfn/11" rel="profile"/>
<style id="jetpack-boost-critical-css">@media all{
...

>>> soup.body     
<body class="home blog wp-embed-responsive post-image-below-header 
post-image-aligned-center left-sidebar nav-below-header separate-containers 
fluid-header active-footer-widgets-0 nav-search-enabled nav-aligned-left 
header-aligned-left dropdown-hover" data-rsssl="1" 
itemscope="" itemtype="https://schema.org/Blog">
...

>>> soup.body.a
<a class="screen-reader-text skip-link" href="#content" 
title="Skip to content">Skip to content</a>

>>> for link in soup.find_all('a'):
        print(link.get('href'))
 
#content
https://automattic.com/cookies/
https://improveandrepeat.com/
#
https://ImproveAndRepeat.com/
https://improveandrepeat.com/about/
#
https://improveandrepeat.com/2022/08/the-split-phase-refactoring/
https://improveandrepeat.com/author/jg/
https://improveandrepeat.com/tag/testing/
https://improveandrepeat.com/2022/08/python-friday-136-date-and-time-in-python-part-3-dateutil/
...

