# encoding:utf-8
from pathlib import Path
import json
import requests
import re
from readability.readability import Document
from bs4 import BeautifulSoup
import pandas as pd



path1 = Path( r"C:\Users\F-CUI\Desktop\ZEW\policy-extraction-github\viewer" ) # path of decisions.json
path = r"C:\Users\F-CUI\Desktop\ZEW\26" # path of 26
pathtest = r"C:\Users\F-CUI\Desktop\ZEW\test html"
print(path1 / 'decisions.json')
with open(path1 / 'decisions.json','r') as load_f:
    for line in load_f:
        load_dict = json.loads(line)
        if load_dict['isGood']=='False': # check the result of extraction
            print(load_dict['id'])
            # df = pd.read_csv(path+"\\" + load_dict['id'][:13] + ".csv", encoding="utf-8")
            # # df = pd.read_csv(path / file, encoding="utf-8")
            # print(df)
            # withinindex = int(load_dict['id'][-2:])
            # print(df.loc[withinindex,'html'])
            # print(222)
            # csvinfo = str(df.loc[withinindex,'html'])
            # print(csvinfo)
            # print(111)

            # doc = Document(csvinfo)
            # readable_article = doc.summary()

            # f = open(pathtest+"/"+load_dict['id']+'.html','w',encoding="utf-8")
            # f.write(readable_article)
            # f.close()

