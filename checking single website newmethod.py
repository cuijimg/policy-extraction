
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
from readability import Document

from flask import Flask

import os

import citations

from pathlib import Path

app = Flask(__name__)


csv.field_size_limit(500 * 1024 * 1024)


def score_text(text: str) -> int:
    words = ''.join(filter(lambda x: x.isalpha() or x.isspace(), text))
    # words = set(words.split(' '))
    words = words.split(' ')
    score = 0

    for word in words:
        if word in keywords:
            score += 1
    # for keyword in keywords:
    #     if keyword in words:
    #         score += 1
    return score


def trim_node(root):
    viable_children = []
    global counter 
    
    for child in root.children:
        if type(child) is not bs4.element.Tag:
            continue
        child['style'] = 'border: 4px solid black;' # debug
        if counter==4:
            child['style'] = 'border: 4px solid green;' # debug
        if counter==5:
            child['style'] = 'border: 4px solid blue;' # debug
            
        if counter==6:
            child['style'] = 'border: 4px solid brown;' # debug
            print('child score is',score_text(child.get_text()))
        if score_text(child.get_text()) >= THRESHOLD:
            viable_children.append(child)
            
    if counter==6:
        print('the lenth is',len(viable_children))
    if len(viable_children) == 0:
        return None
    elif len(viable_children) == 1:
        print(111)
        counter += 1
        return trim_node(viable_children[0])
    else:
    # elif len(viable_children) == 2:
    #     return trim_node(viable_children[0])

    # elif len(viable_children) >= 3:
        print(len(viable_children))
        root['style'] = 'border: 4px solid red;'
        return root
    
    
    
keywords=set(['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
          'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
          'Datenschutzbeauftragter','Datenschutzbeauftragten',
          'Personenbezogene','Personenbezogener','Daten',
          'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
          'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics'])
def res2(match):
    """This function replaces the found citation with a span element with different background."""
    return f'<span style="background: blue;">{match.group()}</span>'


def highlight(exp,res, input: str) -> str:
    """This function takes the html as string, matches all regular expressions and replaces the span elements."""
    return exp.sub(res, input)



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

        # cleaning unicode encoding special character '�'
        csvinfo = csvinfo.replace('�','y')
        
        if csvinfo != 'nan':
            
            # Method 1
            doc = Document(csvinfo)
            readable_article = doc.summary()

            # Method 2
            soup = BeautifulSoup(csvinfo, 'lxml')
            THRESHOLD = 4 
            counter = 0
            res = trim_node(soup)
            while soup.find_all(attrs={'style':'border: 4px solid red;'}) == []: 
                THRESHOLD -= 1
                print('threshold is',THRESHOLD)
                if THRESHOLD == 0:
                    break               
                counter = 0
                res = trim_node(soup)

            # writing in to html
            f = open(path+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")
            f.write(readable_article)
            f.close()

            f = open(path+"/"+file.strip('.csv')+'1'+'.html','w',encoding="utf-8")
            f.write(str(soup))
            f.close()
            # break    
    break

