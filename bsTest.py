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
parj Str. 51
<br>
gog Strasse 51
<br>
10789 Berlin abcdefghijklmnopqrstuvwxyz
<br>
Deutschland
<br>
Tel.: 030/211300-1
<br>
E-Mail: mail@franzimmobilien.de
<br>
Website: www.franzimmobilien.de
</p>

<p>
Lietzenburger Straße 51
</p>
<p>
Art.101 jiji DSGVO
</p>
<p>
parj Str. 51
</p>
<p>
gog Strasse 51
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
# trim(soup)
# This is the reworked regex. I only had to change a few minor things.
exp = re.compile(r'\b(art[.]?|arti[a-z]+|§)\W+(?:\w+\W+){1,10}(ds[-]*g[-]*vo|bdsg|Datenschutzgrundverordnung|TMG)\b', re.IGNORECASE)


def res(match):
    """This function replaces the found citation with a span element with yellow background."""
    return f'<span style="background: purple">{match.group()}</span>'

def res2(match):
    """This function replaces the found citation with a span element with yellow background."""
    return f'<span style="background: green">{match.group()}</span>'


def highlight(exp,res,input: str) -> str:
    """This function takes the html as string, matches all regular expressions and replaces the span elements."""
    return exp.sub(res, input)

patternlist = {"website:.*","^\nE-Mail:.*","Deutschland","[0-9]{5}[\s|\w]{1,10}",".*gmbh.*",".*Straße.*",".*Strasse.*","E-Mail:.*","Tel\..*",".*str\..*"}
    # for pattern in patternlist:
    #     for ele in soup.find_all(text=re.compile(pattern,re.I)):
    #         if len(ele)<30:
    #             ele.parent['style'] = 'background-color: blue; color: yellow'
    #         # ele.extract()
for pattern in patternlist:
    text=re.compile(pattern,re.I)
    soup = highlight(text,res2,str(soup))
    
print(str(soup))    
# Highlight citations
soup = highlight(exp,res,str(soup))
print(soup)
print(1)
soup = bs4.BeautifulSoup(soup, 'lxml')
print(soup)
filtered_list = soup.find_all(attrs={'style':'background: green'})
               
recele = filtered_list[0]
while recele != filtered_list[len(filtered_list)-1] and recele != None:
    recele = recele.next_sibling
    if type(recele) is bs4.element.Tag:
        recele['style'] = 'background: green;'
        print(recele)
        print(1)
print(soup)