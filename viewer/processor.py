# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:36:21 2021

@author: F-CUI
"""
import bs4
import re


def score_text(text: str) -> int:
    words = ''.join(filter(lambda x: x.isalpha() or x.isspace(), text))
    words = set(words.split(' '))
    score = 0
    for keyword in keywords:
        if keyword in words:
            score += 1
    return score


def trim_node(root):
    viable_children = []
    for child in root.children:
        if type(child) is not bs4.element.Tag:
            continue
        if score_text(child.get_text()) >= THRESHOLD:
            viable_children.append(child)
    if len(viable_children) == 0:
        return None
    elif len(viable_children) == 1:
        return trim_node(viable_children[0])
    else:
        root['style'] = 'border: 4px solid red;'
        return root


def trim_node1(root):
    for child in root.contents:
        if type(child) is bs4.element.NavigableString:
            if score_text(str(child))>1:
                child.parent['style'] = 'border: 3px solid orange;'
            continue
        if type(child) is not bs4.element.Tag:
            continue
        if len(child.contents)>1:
            trim_node1(child)
        else:
            if score_text(child.get_text())>0:
                child['style'] = 'border: 3px solid orange;'
                  
keywords=['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
      'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
      'Datenschutzbeauftragter','Datenschutzbeauftragten',
      'Personenbezogene','Personenbezogener','Daten',
      'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
      'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics']

# THRESHOLD = 4

# This is the reworked regex. I only had to change a few minor things.
regexp = re.compile(r'\b(art[.]?|arti[a-z]+|§)\W+(?:\w+\W+){1,10}(ds[-]*g[-]*vo|bdsg|Datenschutzgrundverordnung|TMG)\b', re.IGNORECASE)


def res1(match):
    """This function replaces the found citation with a span element with different background."""
    return f'<span style="background: purple; color: yellow">{match.group()}</span>'

def res2(match):
    """This function replaces the found citation with a span element with different background."""
    return f'<span style="background: green;">{match.group()}</span>'


def highlight(exp,res, input: str) -> str:
    """This function takes the html as string, matches all regular expressions and replaces the span elements."""
    return exp.sub(res, input)

def process(html):
    # Draw a box around policy content
    soup = bs4.BeautifulSoup(html, 'lxml')
    
    #Threshold decreasing method: if nothing is captured, decrease the threshold by 1
    global THRESHOLD
    THRESHOLD = 4
    res = trim_node(soup)
    while soup.find_all(attrs={'style':'border: 4px solid red;'}) == []: 
        THRESHOLD -= 1
        if THRESHOLD == 0:
            break
        res = trim_node(soup)
    # res = trim_node(soup)
    # if soup.find_all(attrs={'style':'border: 4px solid red;'}) == []:
    #     trim_node1(soup)
    #     filtered_list = soup.find_all(attrs={'style':'border: 3px solid orange;'})
    #     if len(filtered_list)>=3:
    #         filtered_list[2].parent['style'] = 'border: 4px solid green;'
    #     if len(filtered_list)>=4:
    #         filtered_list[3].parent['style'] = 'border: 4px solid green;'
    #     if len(filtered_list)>=5:
    #         filtered_list[4].parent['style'] = 'border: 4px solid green;'
  
    
    # Highlight titles
    # Pattern 1: with the tag 'strong'
    strongcontents = soup.find_all('strong')
    for strongcontent in strongcontents:
        if len(strongcontent.text)>0:
            if strongcontent.text [-1] not in {'?','.'} and strongcontent.text[-2:] not in {'an'}:
                strongcontent['style'] = 'background-color: yellow; color: black'
    
    # Pattern 2: with heading tags
    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    for tags in soup.find_all(heading_tags):
        tags['style'] = 'background-color: yellow; color: black'
    
    # # Mark contact information
    # patternlist = {"telefax:.*","email:.*","telefon:.*","website:.*","^\nE-Mail:.*","Deutschland","[0-9]{5}[\s|\w]{1,20}",".*gmbh",".*Straße.*",".*Strasse.*",".*Fax.*","E-Mail:.*","Tel\..*",".*str\..*"}
    # # for pattern in patternlist:
    # #     for ele in soup.find_all(text=re.compile(pattern,re.I)):
    # #         if len(ele)<30:
    # #             ele.parent['style'] = 'background-color: blue; color: yellow'
    # #         # ele.extract()
    # for pattern in patternlist:
    #     text = re.compile(pattern,re.I)
    #     soup = highlight(text,res2,str(soup))
    #     soup = bs4.BeautifulSoup(soup, 'lxml')
    
    # Highlight citations
    soup = highlight(regexp,res1,str(soup))
    soup = bs4.BeautifulSoup(soup, 'lxml')

    return soup