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


csv.field_size_limit(500 * 1024 * 1024)


import os
path = r"C:\Users\f-cui\Desktop\ZEW\26" 
files= os.listdir(path) 
s = []
count = 0
for file in files: 
    print(file)
    if not os.path.isdir(file): 
        with open(path+"/"+file,'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            column = [row[5] for row in reader]
            # print(column)
            #  count+=1
            # print(count)
        
        for csvinfo in column:
            if csvinfo != '0':
                print(csvinfo)
                print(89)
                soup = BeautifulSoup(csvinfo, 'lxml')
#                print(soup.prettify)
                children = soup.find_all()
#                children = soup.findChildren()
#                children = soup.children
                print(children)
                print(66)
                for child in children:
                    print(child)
                    print(111)
                    text = child.get_text()
                    print(text)
                    print(222)
                
            
    break