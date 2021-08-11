
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
    

    
keywords=['Datenschutzerklärung','Datenschutz','Datenschutzhinweise',
          'EU-Datenschutz¬grundverordnung','Datenschutzbeauftragte',
          'Datenschutzbeauftragter','Datenschutzbeauftragten',
          'Personenbezogene','Personenbezogener','Daten',
          'Verarbeitung','personenbezogenen','DSGVO','DS-GVO',
          'Rechte','Auskunft','Auskunftsrecht','Recht','Analytics']


from pathlib import Path
path = Path( r"E:\policies_output" )
folders= [format(i, '#04x')[2:4] for i in range(256)]
folders_given = [g.name for g in path.glob('*')]
if all([f in folders_given for f in folders]): # check if the folders are correct
    for folder in folders:
        path = path / folder
        files = list(path.glob("*.csv"))
        print(files)
        
        for file in files: 
            print(file) 
            df = pd.read_csv(file, index_col=0, encoding="utf-8")
            df['content'] = ''
            for index, row in df.iterrows():
                html = row['html']
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
                        
                    box = soup.find(attrs={'style':'border: 4px solid red;'})
                    if box != None:
                        df.loc[index,'content'] = box.get_text()   
            print(df['content'])
            df.to_csv(file, encoding="utf-8")
            
            # # for further check
            # df = pd.read_csv(file,usecols=['content'], encoding="utf-8") 
   


