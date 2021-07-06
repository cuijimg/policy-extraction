# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 14:13:26 2021

@author: Jimmy Cui
"""
import bs4
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url='http://www.pythonscraping.com/pages/page3.html'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
children = soup.find('table',{'id':'giftList'}).children

#content = soup.find('table',{'id':'giftList'})
#children = content.findChildren()

descendants = soup.find('table',{'id':'giftList'}).descendants
sum = 0
for child in children:
    print(sum)
    print(child)
    sum +=1
print(sum)
#sum2 = 0
#for descendant in descendants:
#    print(sum2)
#    print(descendant)
#    sum2+=1
#print(sum2)
