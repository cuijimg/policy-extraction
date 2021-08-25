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


csv.field_size_limit(500 * 1024 * 1024)

# remove unicode and ascii, make the html xml-readable
def remove_control_characters(html):
    def str_to_int(s, default, base=10):
        if int(s, base) < 0x10000:
            return chr(int(s, base))
        return default
    html = re.sub(u"&#(\d+);?", lambda c: str_to_int(c.group(1), c.group(0)), html)
    html = re.sub(u"&#[xX]([0-9a-fA-F]+);?", lambda c: str_to_int(c.group(1), c.group(0), base=16), html)
    html = re.sub(u"[\x00-\x08\x0b\x0e-\x1f\x7f]", "", html)
    return html

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
folders= [format(i, '#04x')[2:4] for i in range(256)] # generating a list of the folder names in the format of #04x
folders_given = [g.name for g in path.glob('*')]
if all([f in folders_given for f in folders]): # check if the folders are correct
    for folder in folders:
        
        path = Path( r"E:\policies_output" ) / folder
        files = list(path.glob("*.csv"))
        print(folder, path)
        # print(files)
        
        for file in files: 
            print(folder, file)
            df = pd.read_csv(file, index_col=0, encoding="utf-8")
            df['content'] = ''
            for index, row in df.iterrows():
                html = row['html']
                csvinfo = str(html)

                # cleaning unicode encoding special character '�'
                csvinfo = csvinfo.replace('�','y')

                csvinfo = remove_control_characters(csvinfo)

                if csvinfo != 'nan':
                    # # Method 1
                    # soup = BeautifulSoup(csvinfo, 'lxml')
                    # THRESHOLD = 4 
                    # res = trim_node(soup)  
                    # while soup.find_all(attrs={'style':'border: 4px solid red;'}) == []: 
                    #     THRESHOLD -= 1
                    #     if THRESHOLD == 0:
                    #         break
                    #     res = trim_node(soup)
                    #     print(THRESHOLD)
                        
                    # box = soup.find(attrs={'style':'border: 4px solid red;'})
                    # if box != None:
                    #     df.loc[index,'content'] = box.get_text()   

                    # Method 2: using 'readability' package
                    doc = Document(csvinfo)
                    try:
                        readable_article = doc.summary() # extracting the text from html
                        soup = BeautifulSoup(readable_article,'lxml')
                        df.loc[index,'content'] = soup.get_text()
                    except ValueError as e:
                        print(e)


            # print(df['content'])
            df.to_csv(file, encoding="utf-8")
            
            # # for further check
            # df = pd.read_csv(file,usecols=['content'], encoding="utf-8") 
            # print(df['content'])
            # break
   


