# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:36:21 2021

@author: F-CUI
"""
import bs4


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
        root['style'] = 'border: 1px solid red;'
        return root

keywords=['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
      'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
      'Datenschutzbeauftragter','Datenschutzbeauftragten',
      'Personenbezogene','Personenbezogener','Daten',
      'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
      'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics']

THRESHOLD = 2


def process(html):
    # I know that html is not nan, since I check for that in the calling function.
    # Therefore, I can simplify this function.
    soup = bs4.BeautifulSoup(html, 'lxml')
    res = trim_node(soup)
    
    strongcontents = soup.find_all('strong')
    for strongcontent in strongcontents:
        if len(strongcontent.text)>0:
            if strongcontent.text[-1] not in {'?','.'} and strongcontent.text[-2:] not in {'an'}:
                strongcontent['style'] = 'background-color: yellow; color: black'
    
    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    for tags in soup.find_all(heading_tags):
        tags['style'] = 'background-color: yellow; color: black'
    return soup