#coding = utf-8
from urllib import urlopen
from urllib import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import sys,os
import re

'''
    重点关注多线程
'''

savepath=r"D://tbmm"

def mkdir(path):
    if os.path.exists(path):
        return
    os.mkdir(path)

# 获取每个模特的个性域名
def getUrls(url):
    driver= webdriver.PhantomJS()
    html = urlopen(url)
    bs = BeautifulSoup(html.read().decode('gbk'),"html.parser")
    girls = bs.findAll("a",{"class":"lady-name"})
    namewithurl = {}
    for item in girls:
        linkurl = item.get('href')
        driver.get("https:"+linkurl)   #为什么非也要用这种方式获得
        bs1 = BeautifulSoup(driver.page_source,"html.parser")
        links = bs1.find("div",{"class":"mm-p-info mm-p-domain-info"})
        if links is not None:
            links = links.li.span.get_text()
            namewithurl[item.get_text()] = links
            print(links)
    return namewithurl

def getImgs(parms):
    personname = parms[0]
    personurl = "https:"+parms[1]
    html = urlopen(personurl)
    bs = BeautifulSoup(html.read().decode('gbk'),"html.parser")
    contents = bs.find("div",{"class":"mm-aixiu-content"})
    imgs = contents.findAll("img",{"src":re.compile(r'//img\.alicdn\.com/.*\.jpg')})
    savefilename = os.path.join(savepath,personname)
    mkdir(savefilename)
    print("img num :",len(imgs))
    cnt = 0
    for img in imgs:
        try:
            urlretrieve(url = "https:"+img.get("src"),filename =os.path.join(savefilename,str(cnt)+".jpg"))
            cnt+=1
        except Exception,e:
            continue

if __name__ == "__main__":
    urls = getUrls("https://mm.taobao.com/json/request_top_list.htm?page=1")
    pool = ThreadPool(4)
    pool.map(getImgs,urls.items())
    pool.close()
    pool.join()
    # for (k,v) in urls.items():
    #     getImgs((k,v))
