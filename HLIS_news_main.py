import requests
import chardet
from bs4 import BeautifulSoup
import facebook
import time

cfg = {
 "page_id" : "328183278116459", # Step 1
 "access_token" : "EAAGK96361AABAD95yWF7MMczMoufybwzTBYn6cSiq0LhrH22G3jhZAqiJIevpZApwSfjsrMdkAZBBjXuUNR0zpwTcjrRt0V39NJpLpi9czVCxoWMGH5OcjYsixhP9qhFiHZBouWAsZCJnxGr8jIZCJ2s8c7S2fglrOsi8T03aZC8AZDZD" #step3
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

    for s in sel:
    #s = sel[0]
        #for begin
        data = {}
        
        #abstract title & url
        atag = s.select("a")
        data["title"] = atag[0]["title"]
        data["url"] = atag[0]["href"]
        
        #abstract issuer
        
        data["issuer"]  = s.select("td")[1].text.strip()
        
        #abstract date
        
        data["date"]  = s.select("td")[2].text.strip()
        
        filt(data)
        
        #for end
    
    return

def filt(data):
    
    print(data)
    
    publisher({
        "message":'#'+data['issuer']+' / '+data['title']+' / '+data['date'],
        "link":data["url"]
    });
    
    return

def publisher(content):
        
    #post text,link
    print(graph.put_object(cfg['page_id'],"feed",message=content["message"],link=content["link"]))
    
    time.sleep(20)
    return

getrawlist()