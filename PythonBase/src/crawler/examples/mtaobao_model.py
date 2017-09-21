#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:多进程(进程池)-下载淘宝模特图片
    Ref:http://www.cnblogs.com/haoliuhust/p/5759339.html
    Author:tuling56
    Date:2017年9月21日
'''


import re
import os,sys
import time
from datetime import date, datetime, timedelta

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')


import json
from urllib import urlopen
from urllib import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool


savepath=r"D:\\Trash\\tbmm"

# 获取每个模特的个性域名，返回每个模特名和对应的主页的字典
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

    print json.dumps(namewithurl,ensure_ascii=False)

    return namewithurl



# 下载该模特的所有图片
def getImgs(parms):
    personname = parms[0].encode('gbk')
    personurl = "https:"+parms[1]
    html = urlopen(personurl)
    bs = BeautifulSoup(html.read().decode('gbk'),"html.parser")
    contents = bs.find("div",{"class":"mm-aixiu-content"})
    imgs = contents.findAll("img",{"src":re.compile(r'//img\.alicdn\.com/.*\.jpg')})
    personpath = os.path.join(savepath,personname)
    if not os.path.exists(personpath):
        os.mkdir(personpath)

    print "%s img num : %s" %(personname,len(imgs))

    for cnt,img in enumerate(imgs):
        try:
            rurl="https:"+img.get("src")
            fname=os.path.join(personpath,str(cnt)+".jpg")
            print fname
            urlretrieve(url =rurl ,filename =fname)
        except Exception,e:
            print str(e)



# 测试入口
if __name__ == "__main__":
    urls = getUrls("https://mm.taobao.com/json/request_top_list.htm?page=1")
    pool = ThreadPool(4)
    pool.map(getImgs,urls.items())
    pool.close()
    pool.join()
    # for (k,v) in urls.items():
    #     getImgs((k,v))
