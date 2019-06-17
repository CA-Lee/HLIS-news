#!/usr/bin/env python
# coding: utf-8

# In[177]:


import requests
import chardet
from bs4 import BeautifulSoup

#r = requests.get("https://www.ptt.cc/bbs/MobileComm/index.html")
r = requests.get("http://bcc.hlis.hlc.edu.tw/files/40-1000-12-1.php")
r.encoding = 'utf-8'
#print(r.text)

soup = BeautifulSoup(r.text,"html.parser")
#print(soup.text)

sel = soup.select("table.baseTB.listTB.list_TABLE.hasBD.hasTH tbody tr")
#print(sel)

for s in sel:
    #for begin
    
    data={}
    
    #abstract title & url
    atag = s.select("a")
    data["title"] = atag[0]["title"]
    data["url"] = atag[0]["href"]
    
    #abstract issuer
    
    data["issuer"]  = s.select("td")[1].text.strip()
    
    #abstract date
    
    data["date"]  = s.select("td")[2].text.strip()
    
    print(data["date"],"/",data["issuer"],"/",data["title"],"\n",data["url"])
    
#for end


# In[144]:


import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.ptt.cc/bbs/MobileComm/index.html") #將網頁資料GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
sel = soup.select("div.title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
for s in sel:
    #print(s["href"], s.text) 
    print(s)

