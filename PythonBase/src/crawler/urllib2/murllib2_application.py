#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能：urllib2库的应用之下载mp3
    ref:
    state:
'''

import re
import urllib,urllib2
import json
from collections import OrderedDict

import socket
socket.setdefaulttimeout(60)    # 设置全局socket超时时间60s


'''
    应用：获取和下载MP3
    功能注释：下载和保存固定网址的mp3视频,主要是urlib2库的使用
'''
class ExDownMP3():
    def __init__(self):
        self.entry_url="http://www.tingshuge.com/Book/2379.html"

    # 首先获取全部的url（带header头）
    def getAllURL_api(self):
        regex=re.compile(r'/down/\?2379-\d{1,3}\.html')
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent' : user_agent}
        request = urllib2.Request(self.entry_url,None,headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError,e:
            print e.reason
        content= response.read().decode('gbk')
        resl=re.findall(regex,content)
        return  resl

    # 对每个url进行处理
    def getMp3_api(iurl):
        url = "http://www.tingshuge.com"+iurl;
        numr=re.search(r'(?<=-)\d{1,3}(?=\.html)',iurl)
        if numr:
            num=int(numr.group())+1
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent' : user_agent}
        request = urllib2.Request(url,None,headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError,e:
            print e.reason
        page = response.read().decode('gbk')
        pattern = re.compile(r"http://audio\.kting\.cn/Other/Sample_Audio.*\.mp3")
        rest=re.search(pattern,page)
        if rest:
            bytes1=urllib2.urlopen(rest.group())
            f = open("D://"+str(num)+".mp3", 'wb')  # 全部读取然后保存的
            f.write(bytes1.read())      # 利用url打开音频的地址，然后二进制写入
            f.flush()
            f.close()

    #入口：下载音频
    def down_mp3_entry(self):
        allurl=self.getAllURL_api(self.entry_url)
        for url in allurl:
            self.getMp3_api(url)


# 测试入口
if __name__ == "__main__":
    ed3=ExDownMP3()
    ed3.down_mp3_entry()


