# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:36:21 2021

@author: F-CUI
"""


def next_result(self):
    
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
    
    for html in html_list: # html_list contains the list of all websites that we extract in a csv file
        csvinfo = str(html)      
        if csvinfo != 'nan':
            soup = BeautifulSoup(csvinfo, 'lxml')
            res = trim_node(soup)
            
        if res is None:
            THRESHOLD = 1
            csvinfo= csvinfo.replace("<br>","\n")
            if csvinfo != 'nan':
                soup = BeautifulSoup(csvinfo, 'lxml')
                res = trim_node(soup)
    return res