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
app = Flask(__name__)


csv.field_size_limit(500 * 1024 * 1024)

def grade(keywordlist,text): # word check
    text = re.sub('\\.|-|\t|_|%|(|)|％|\(|°|\)|\[|\]|/|“|”|"|"|^|\n','',text)
    text = re.sub(r'{|}|<|>|-|:|;|,|[.]|[+]','',text)
    words = re.split(' ',text)
    points = 0
    for i in keywordlist:
        for j in words:
            if i == j:
                points+=1
    return(points)

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
            print(1)
            print(score_text(child.get_text()) )
            viable_children.append(child)
            print(viable_children)
    if len(viable_children) == 0:
        return None
    elif len(viable_children) == 1:
        return trim_node(viable_children[0])
    else:
        root['style'] = 'border: 4px solid red;'
        return root
    
def trim_node1(root):
    # print('executed')
    for child in root.contents:
        print(1)
        print(child)
        print(2)
        if type(child) is bs4.element.NavigableString:
            print('NS')
            if score_text(str(child))>1:
                child.parent['style'] = 'border: 3px solid orange;'
            continue
        if type(child) is not bs4.element.Tag:
            continue
        if len(child.contents)>1:
            trim_node1(child)
        else:
            print('score',score_text(child.get_text()))
            if score_text(child.get_text())>0:
                child['style'] = 'border: 3px solid orange;'
    
keywords=['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
          'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
          'Datenschutzbeauftragter','Datenschutzbeauftragten',
          'Personenbezogene','Personenbezogener','Daten',
          'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
          'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics']

THRESHOLD = 4


import os
import glob

from pathlib import Path
# path = Path( r"C:/Users/F-CUI/Desktop/ZEW/26" )
path = r"C:\Users\F-CUI\Desktop\ZEW\test"
path1 = r"C:\Users\F-CUI\Desktop\ZEW\test"

files= os.listdir(path) 

# files = list(path.glob("*.csv"))
print(files)
s = []
for file in files: 
    print(file)
    contentlist = []
    if not os.path.isdir(file): 
        
        # df = pd.read_csv(path+"/" + file, usecols=['html'], encoding="utf-8")
        df = pd.read_csv(path+"/" + file, encoding="utf-8")
        # df = pd.read_csv(path / file, encoding="utf-8")
        df['content'] = ''
        index = 0
        for html in df['html']:
            csvinfo = str(html)

            
            if csvinfo != 'nan':
                # print(csvinfo_replace)
                soup = BeautifulSoup(csvinfo, 'lxml')
                # print(soup)
                res = trim_node(soup)
                
                if soup.find_all(attrs={'style':'border: 4px solid red;'}) == []:
                    trim_node1(soup)
                    
                print(res)
                
                if res is not None:
                    contentlist.append(res.get_text())
                print(contentlist)
                
                f = open(path1+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")
                f.write(str(soup))
                f.close()
                
        #         # htmlpath = file.with_suffix('.html')
        #         # htmlpath.write_text(str(soup))
                
        #         #write the text to a new column in the csv
        #         df.at[index,'content'] = res.get_text()
        #         index += 1
        # df.to_csv(path+"/" + file, encoding="utf-8")
        # df = pd.read_csv(path+"/" + file,usecols=['content'], encoding="utf-8") 
        # # print(df['content'][0])
    break
