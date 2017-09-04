#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python网络文件下载，
    State:后期再结合网页爬虫，实现指定站点的下载
    Author:tuling56
    Date:2016年12月29日
'''
import os,sys
import time
import traceback
from datetime import date, datetime, timedelta
import urllib


reload(sys)
sys.setdefaultencoding('utf-8')


# 显示执行进度
def Schedule(a,b,c):
    '''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100

    print '%.2f%%' % per



# url根据url下载文件和选择保存
def down_load(down_url):
    try:
        save_file=down_url.split('/')[-1]
        urllib.urlretrieve(down_url,save_file,Schedule)
        '''
        response = urllib2.urlopen(get_down_url)
        data=response.read()

        f=open(filename,'wb')
        print filename
        f.write(data)
        '''
    except Exception,e:
        traceback.print_exc()
        print 'timeout...'


'''
    主入口
'''
if __name__ == "__main__":
    down_url="http://bugreport.xunlei.com:21212/0x800/2016-12-22/1.0.0.1/C5-03049CDD-0B77DECD-080E5FFD.zip"
    down_load(down_url)

