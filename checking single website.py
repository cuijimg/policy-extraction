
#coding=utf-8
"""
Created on Mon Jul  5 12:25:16 2021

@author: Jimmy Cui
"""
import bs4
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re
from flask import Flask

import os

import citations

from pathlib import Path

app = Flask(__name__)


csv.field_size_limit(500 * 1024 * 1024)


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
            print('vialist',viable_children)
    if len(viable_children) == 0:
        return None
    elif len(viable_children) == 1:
        print(111)
        return trim_node(viable_children[0])
    else:
        print(len(viable_children))
        root['style'] = 'border: 4px solid red;'
        return root
    

    
keywords=['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
          'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
          'Datenschutzbeauftragter','Datenschutzbeauftragten',
          'Personenbezogene','Personenbezogener','Daten',
          'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
          'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics']





# path = Path( r"C:/Users/F-CUI/Desktop/ZEW/26" )
path = r"C:\Users\F-CUI\Desktop\ZEW\test"

files= os.listdir(path) 
# files = list(path.glob("*.csv"))

print(files)
s = []
for file in files: 
    print(file)
    
    df = pd.read_csv(path+"/" + file, encoding="utf-8")
    # df = pd.read_csv(path / file, encoding="utf-8")
    df['content'] = ''
    index = 0
    for html in df['html']:
        csvinfo = str(html)

        
        if csvinfo != 'nan':
            soup = BeautifulSoup(csvinfo, 'lxml')
            THRESHOLD = 4 
            res = trim_node(soup)
            while soup.find_all(attrs={'style':'border: 4px solid red;'}) == []: 
                THRESHOLD -= 1
                if THRESHOLD == 0:
                    break
                res = trim_node(soup)
                print(THRESHOLD)

            citations.replace_html(soup, tag_style='border: 1px solid black')

            # writing in to html
            f = open(path+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")

            f.write(str(soup))
            print(1)
            f.close()
            break    
    break

