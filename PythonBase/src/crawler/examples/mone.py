#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:爬取one的图片和文字
    Ref:http://python.jobbole.com/84714/
    State：使用了多进程
    Date:2016/12/30
    Author:tuling56
'''

import argparse
import re
from multiprocessing import Pool
import requests
import bs4
import time
import json
import io

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



root_url = 'http://wufazhuce.com'

def get_url(num):
    return root_url + '/one/' + str(num)

def get_urls(num):
    urls = map(get_url, range(100,100+num))
    return urls

def get_data(url):
    dataList = {}
    response = requests.get(url)    #利用requests获取网页内容
    if response.status_code != 200:
        return {'noValue': 'noValue'}
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    # 获取索引号
    dataList["index"] = soup.title.string[4:7]
    # 获取内容
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = meta.get('content')
    # 获取图像地址
    dataList["imgUrl"] = soup.find_all('img')[1]['src']
    return dataList

# 测试入口
if __name__=='__main__':
    pool = Pool(4)
    dataList = []
    urls = get_urls(2)
    start = time.time()
    dataList = pool.map(get_data, urls)
    end = time.time()
    print 'use: %.2f s' % (end - start)

    '''方法1
    jsonData = json.dumps({'data':dataList},ensure_ascii=False,encoding='utf8')
    with open('myonedata.txt', 'w') as outfile:
        json.dump(jsonData, outfile,encoding='utf8',ensure_ascii=False)
    '''

    with open('myonedata.txt', 'w') as f:
        json.dump({'data':dataList},f,ensure_ascii=False)


