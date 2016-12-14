#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''

import urllib2
import json
import MySQLdb
import sys

toplist=[]
# 获取播放次数最高的256部视频(cid+filesize)
def gettop():
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='xmp', passwd='view_hot',db='xmp_hot_view')
    if not conn.open:
        print('open connnection fail')
        exit()
    cur = conn.cursor()
    cur.execute('set names utf8;')

    infostr=""
    for i in range(0, 256):
        table='hot_view_%02X' % i
        try:
            sql = "select cid,filesize from {table}  order by view_num desc limit 1;".format(table=table);
            print(sql)
            cur.execute(sql)
            querydata = cur.fetchone()
            toplist.append(querydata)
            infostr+=querydata[0]+'.'+str(querydata[1])+'\n'
        except Exception,e:
            derror=sys.exc_info()
            print "error-->%s,line:%s" %(derror[1],derror[2].tb_lineno)
    cur.close()
    conn.close()

    # 存文件
    fout=open('toplist','w')
    fout.write(infostr)
    fout.close()
    return  toplist;


'''
   {"hot_view":[3108,3147,3162,2908,2762,2644,2536,2462,2401,2349,2319,2282,2240,2203,"ext":".rmvb"}
    url='http://media.v.xunlei.com/pc/id_mapping?media_type=|tv|anime|teleplay|movie'
    url='http://hotview.v.xunlei.com/3F/03/3F035A5C6FBA744BDD1893E67E5D4016F9731918.1602770288'
'''

def getview():
    for item in toplist:
        cid,filesize=item
        url="http://hotview.v.xunlei.com/"+cid[0:2]+"/"+cid[2:4]+"/"+cid+"."+filesize
        resonse=urllib2.urlopen(url)
        content=resonse.read().decode('utf8')
        viewdata=json.loads(content)
        views=viewdata.get('hot_view','')
        if views:
            return  views
            #处理每一个数据
    return 0;


if __name__ == "__main__":
    gettop()
    #getview()
