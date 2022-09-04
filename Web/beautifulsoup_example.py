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


>>> contacts = """
<html>
<head>
	<title></title>
</head>
<body>
	<h1>Contact</h1>
	<table>
		<tr>
			<th>name</th>
			<th>phone</th>
			<th>country</th>
			<th>email</th>
		</tr>
		<tr>
			<td>Harlan Gibbs</td>
			<td>1-351-733-8608</td>
			<td>Chile</td>
			<td>nec.quam.curabitur@outlook.net</td>
		</tr>
		<tr>
			<td>Marny Ashley</td>
			<td>1-760-796-7925</td>
			<td>South Korea</td>
			<td>pellentesque@google.edu</td>
		</tr>
		<tr>
			<td>Chava Dixon</td>
			<td>1-828-824-7717</td>
			<td>Switzerland</td>
			<td>malesuada.fames.ac@yahoo.ca</td>
		</tr>
	</table>
 </body>
 </html>
 """

>>> soup = BeautifulSoup(contacts, 'html.parser')
>>> table = soup.body.table
>>> for row in table.find_all('tr'):
      columns = row.find_all('td')
      if columns:
          print(columns[3].text)

nec.quam.curabitur@outlook.net
pellentesque@google.edu
malesuada.fames.ac@yahoo.ca

>>> for row in table.find_all('tr'):
       print(50*'-') 
       headers = row.find_all('th')
       for header in headers:
           print(f'**{header.text}**')
       columns = row.find_all('td')
       for column in columns:
           print(column.text)

————————————————–
**name**
**phone**
**country**
**email**
————————————————–
Harlan Gibbs
1-351-733-8608
Chile
nec.quam.curabitur@outlook.net
————————————————–
Marny Ashley
1-760-796-7925
South Korea
pellentesque@google.edu
————————————————–
Chava Dixon
1-828-824-7717
Switzerland
malesuada.fames.ac@yahoo.ca