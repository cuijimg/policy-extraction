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


import os
path = r"C:\Users\f-cui\Desktop\ZEW\26" 
files= os.listdir(path) 
s = []
threshhold = 1
for file in files: 
    print(file)
    if not os.path.isdir(file): 
        
        df = pd.read_csv(path+"/" + file, usecols=['html'], encoding="utf-8")
        
      
        for html in df['html']:
            csvinfo =str(html)
            if csvinfo != 'nan':
                
                soup = BeautifulSoup(csvinfo, 'lxml')
                res = trim_node(soup)
                print(res)
                f = open(path+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")
                f.write(str(soup))
                f.close()
            
    break
