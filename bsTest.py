# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import bs4
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<strong>paragragh 1</strong>
<strong></strong>
<strong>9. Empfehlung zur Sicherheit Ihrer Bewerberdaten</strong>
<strong>fkjdjfkd an</strong>
<strong>Where is the man?</strong>
<strong>Strafe</strong>
<strong>Attention.</strong>
<h2>paragragh 1</h2>
<h3>Where is the man?</h3>
<h4>Attention.</h4>
<p class="title"><b>The Dormouse's story</b></p>
<p>
Franz Immobilien GmbH
<br>
Lietzenburger Straße 51
<br>
10789 Berlin
<br>
Deutschland
<br>
Tel.: 030/211300-1
<br>
E-Mail: mail@franzimmobilien.de
<br>
Website: www.franzimmobilien.de
</p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
</body>
</html>

"""
import re
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
tel = soup.find_all(text=re.compile("^\nTel.*"))

patternlist = ["^\nTel.*","^\nE-Mail.*",".*Straße.*|str\..*"]
for pattern in patternlist:
    for ele in soup.find_all(text=re.compile(pattern,re.I)):
        ele.parent['style'] = 'background-color: blue; color: yellow'
        # ele.extract()

# print(len(soup.contents[1].contents[2].contents[5].contents))

# for child in soup.contents[1].contents[2].contents[5].contents:
#     print(1)
#     print(child, type(child))

def trim(root):
    for child in root.contents:
        if type(child) is  bs4.element.NavigableString:
            print(2)
            print(str(child))
            print(child.parent)
            print(3)
            continue
        if len(child.contents)>1:
            print(1)
            print(child.contents)
            trim(child)
        else:
            print(child.get_text())
trim(soup)

