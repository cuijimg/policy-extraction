# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 15:57:21 2021

@author: F-CUI
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
import glob

from pathlib import Path
# path = Path( r"C:/Users/F-CUI/Desktop/ZEW/26" )
path = r"C:\Users\F-CUI\Desktop\ZEW\26"
path1 = r"C:\Users\F-CUI\Desktop\ZEW\26html"

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

         
            # if csvinfo != 'nan':
                # print(csvinfo_replace)
            soup = BeautifulSoup(csvinfo, 'lxml')
                # print(soup)
            res = trim_node(soup)
            # print(res)
            
            if res is not None:
                contentlist.append(res.get_text())
                
                for text in res.find_all(text=re.compile("^tel")):
                    print(text)
            # print(contentlist)
                
                # f = open(path1+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")
                # f.write(str(soup))
                # f.close()

                
               
        
        
        #     csvinfo = str(html)

         
        #     if csvinfo != 'nan':
        #         # print(csvinfo_replace)
        #         soup = BeautifulSoup(csvinfo, 'lxml')
        #         # print(soup)
        #         res = trim_node(soup)
        #         print(res)
        #         if res is not None:
        #             contentlist.append(res.get_text())
        #         print(contentlist)
                
        #         f = open(path1+"/"+file.strip('.csv')+'.html','w',encoding="utf-8")
        #         f.write(str(soup))
        #         f.close()
                
        #         # htmlpath = file.with_suffix('.html')
        #         # htmlpath.write_text(str(soup))
                
        #         #write the text to a new column in the csv
        #         df.at[index,'content'] = res.get_text()
        #         index += 1
        # df.to_csv(path+"/" + file, encoding="utf-8")
        # df = pd.read_csv(path+"/" + file,usecols=['content'], encoding="utf-8") 
        # # print(df['content'][0])
    break
