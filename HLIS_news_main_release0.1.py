#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import chardet
from bs4 import BeautifulSoup
import facebook
import time
import re

cfg = {
 "page_id" : "328183278116459", # Step 1
 "access_token" : input('Access_token: ') #step3
}

graph = facebook.GraphAPI(cfg['access_token'])

###############Global setting end###############

def getrawlist():
    
    r = requests.get("http://bcc.hlis.hlc.edu.tw/files/40-1000-12-1.php")
    r.encoding = 'utf-8'
    #print(r.text)

    soup = BeautifulSoup(r.text,"html.parser")
    #print(soup.text)

    sel = soup.select("table.baseTB.listTB.list_TABLE.hasBD.hasTH tbody tr")
    #print(sel)
    
    ret = []

    for s in sel:
    #s = sel[0]
        #for begin
        data = {}
        
        #abstract title & url
        atag = s.select("a")
        data["title"] = atag[0]["title"].strip()
        data["url"] = atag[0]["href"].strip()
        
        #abstract issuer
        
        data["issuer"]  = s.select("td")[1].text.strip()
        
        #abstract date
        
        data["date"]  = s.select("td")[2].text.strip()
        
        ret.append(data)
        
        #for end
    
    return ret

def filt(dataset):
    
    #print(dataset)
    
    #get latest post on facebook page
    r_api = graph.get_object(id=cfg["page_id"],fields="posts.limit(10)")
    #print(r_api)
    
    #find the latest post title
    for i in range(10):
        try:
            last_title = r_api['posts']['data'][i]['message'].strip()
            #print(last_title)
        except KeyError:
            last_title = ""
            
        if last_title != "":
            break
    
    #abstract title
    regex = re.compile(r'[^\/]*\/\s*(.*)\s+\/\s\d{4}\-\d{2}\-\d{2}') #match title
    match = regex.search(last_title)
    #print(type(match))
    
    if match is None:
        last_title = ""
    else:
        last_title = match[1]
    
    #print(last_title)
    
    #search title position
    for index,data in enumerate(dataset):
        if last_title != "" and last_title in data["title"]:
            #print("position:",index)

            #remove all datas after latest posted title(include it) *they're already posted
            for i in range(index,len(dataset)):
                dataset.pop()
                #print("delete:",dataset[i])
    
    #print(dataset)
    
    #make it ready for post
    ret = []
    for data in dataset:
        
        #print(data"\n")        
        
        ret.append({
            "message":'#'+data['issuer']+' / '+data['title']+' / '+data['date'],
            "link":data["url"]
        })
    
    return ret

def publisher(postset):
    
    r_api = []
    postset.reverse()
    for post in postset:
        
        #post text,link
        r = graph.put_object(cfg['page_id'],"feed",message=post["message"],link=post["link"])
        print("result : ",r)
        r_api.append(r)
        
        time.sleep(20)
        
    return r_api

#main

while True:
    
    now = time.localtime(time.time())
    
    print(now.tm_hour," : ",end="")
    
    if now.tm_hour >= 6 and now.tm_hour <= 20:
        
        print("execute")
        
        rawlist = getrawlist()
        #print(rawlist)
        
        ready4post = filt(rawlist)
        print(ready4post)
        
        result = publisher(ready4post)
        #print("result:",result)
        
    else:
        
        print("sleep")
        time.sleep(3600)
    
    time.sleep(600) #run one per ten minutes

