#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：播放排行统计
  改进说明：3.2版本将创建连接部分剥离，编解码进行处理
'''

import MySQLdb
import json
import urllib2
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#########################  Methods ##################################

'''
  初始化工作，打开连接，创建相关表l
'''
def initTable(conn,cur):
    #创建原始表(src_table):存储原始数据
    '''
    fpeerid | fmovieid | ftitle
    '''
    sql='create table if not exists src_table(fpeerid varchar(20),fmovieid varchar(15),ftitle varchar(100)) character set utf8'
    cur.execute(sql)
    conn.commit()

    #创建中间表mid_table1：完成指标uv.pv等指标的统计
    '''
    movieid | title  |  uv |  pv
    '''
    sql='create table if not exists mid_table1(movieid varchar(20),title varchar(30),uv int(10),pv int(10)) character set utf8'
    cur.execute(sql)
    conn.commit()

    #创建中间表mid_table2：将相同movieid的uv和pv数据进行合并
    '''
    movieid |  title | uv | pv
    '''
    sql='create table if not exists mid_table2(movieid varchar(20),title varchar(30),uv int(10),pv int(10)) character set utf8'
    cur.execute(sql)
    conn.commit()

    #创建结果中间表：完成排名关键字外的所有统计
    '''
    日期   影片id   影片类型  影片名   日用户访问  日浏览访问
    mdate | movieid | mtype |  mtitle |  uv     |    pv
    '''
    sql='create table if not exists xmp_day_play_mid(mdate date,movieid varchar(20),mtype varchar(10),mtitle varchar(30),uv int(10),pv int(10)) character set utf8'
    cur.execute(sql)
    conn.commit()

    #创建结果表
    '''
    日期   影片id   影片类型  影片名   日用户访问  日浏览访问 日访问排名
    mdate | movieid | mtype |  mtitle |  uv     |    pv    | morder
    '''
    sql='create table if not exists xmp_day_play(mdate date,movieid varchar(10),mtype varchar(10),mtitle varchar(30),uv int(10),pv int(10),morder int(10)) character set utf8'
    cur.execute(sql)
    conn.commit()


    return conn,cur

'''
   数据准备：数据文件的导出和数据文件加入到数据库src_table表中
'''
def readData(conn,cur,stadate):
    #数据准备(hive数据到本地文件)
    #hivecmd="hive -e \"use kankan_odl;select fpeerid, fmovieid, ftitle from t_stat_play where ds='%s' and fplay_type=2 and length(fmovieid)>4\"> file.txt" %(stadate)
    #os.system(hivecmd)
    #hivecmd="hive -e \"use kankan_odl;select fu1, fu4, '' from xmpconv where ds='%s' and fu3='XMP-JingPin' and length(fu4)>4\" >>file.txt" %(stadate)
    #os.system(hivecmd)

    #导入数据(本地文件导入到MySQL数据库中)
    load_sql="load data local infile '%s' into table '%s'" %('file.txt','src_table') #20150817当天数据载入,如何避免重复导入？？？？
    cur.execute(load_sql)
    conn.commit()


#kankan_dict:由kankan_id反解析movieid
'''
[{"type":"anime","movieid":"mi1000004","kankan_id":"60242"},....,{"type":"movie","movieid":"mi1000006","kankan_id":"63673"}]
由kankan_id反解析movieid
{u'43109': {'movieid': u'mi1114335', 'type': u'movie'},..., u'57230': {'movieid': u'mi1036593', 'type': u'teleplay'}}
'''
url='http://media.v.xunlei.com/pc/id_mapping?media_type=|tv|anime|teleplay|movie'
def urlParase(url):
    resDict={}
    resonse=urllib2.urlopen(url)
    content=resonse.read().decode('utf8')
    plist=json.loads(content) #解析后得到的列表，先转换一下
    for item in plist:
        kankan_id=item['kankan_id']
        if kankan_id!="":
            resDict[kankan_id]={'type':item['type'],'movieid':item['movieid']}
    #print  resDict
    return resDict


#用更新后的movieid去查影片的类型信息和名字
'''
{"background":"http:\/\/i1.media.geilijiasu.com\/b\/d0\/44\/d044d3aceee652b4cad41c84dd1aa330.jpg",
"intro":"","episodes":0,"playtime":"","year":2003,
"poster":"http:\/\/i0.media.geilijiasu.com\/m\/85\/e2\/85e23c50a424f60125b645ae88704aed.jpg",
"rtn":0,"update_status":"",
"area":"美国","genres":"喜剧\/短片","alias":"","actor":"","language":"英语","en_title":"
","douban_score":5,
"type":"movie","director":"Chris Regner",
"title":"Behind the Praise Band: Manna from Heaven",
"is_new":0,"abstract":"",
"movieid":"mi1000220",   #查询起点
"display":"1","imdb_score":0}

'''
def getTypeTitle(movieid):
    url='http://media.v.xunlei.com/pc/info?movieid='+movieid
    headers ={
        "Host":"media.v.xunlei.com",
        "Referer": "http://media.v.xunlei.com",
        "cookie":"client=pc;version=5.1.0.3054"
    }
    request=urllib2.Request(url,None,headers)
    resonse=urllib2.urlopen(request)
    content=resonse.read().decode('utf8')
    pdict=json.loads(content) #解析后得到的字典
    mtype=pdict.get('type','Unknown')
    mtitle=pdict.get('title','Unknown')
    return mtype,mtitle


'''
  中间数据处理：movied解析和去重等
'''
def dataMidPro(conn,cur):
    #填充中间表1的数据
    sql='select fmovieid,ftitle,count(distinct fpeerid) as uv,count(*) as pv  from src_table group by fmovieid having uv>100 order by uv desc'
    cur.execute(sql.encode('utf8')) #Error writing file '/tmp/MY6JCHpZ' (Errcode: 28 - No space left on device)
    conn.commit()
    results=cur.fetchall()
    if(len(results)!=0):
        '''
        mutisql="insert into mid_table1 values ('%s','%s','%s','%s')"
        try:
            cur.executemany(mutisql,results)
            conn.commit()
            print 'data have been insert into mid_table1'
        except Exception,e:
            print(e)
        '''
        for item in results:
            sql="insert into mid_table1 values('%s','%s','%s','%s')" %(item[0],item[1],item[2],item[3])
            cur.execute(sql.encode('utf8'))
            conn.commit()
    else:
        print('=============mid_table1 is empty==============')


    #从中间表1取movieid进行分析
    sql='select movieid from mid_table1'
    cur.execute(sql)
    conn.commit()
    movieid_O=cur.fetchall() #返回的是旧的movieid的元组

    #对movieid进行转化处理分析,配对修改
    movieidmap_ON={}          #旧新movieid对照字典
    resDict=urlParase(url)
    for items in movieid_O:  #取查询结果进行分析
        movieid=items[0]
        if 7==len(movieid):
            new_movieid='mi'+movieid
        elif 5==len(movieid):
            if resDict.get(movieid):
                new_movieid=resDict[movieid]['movieid']  #把movieid作为kankan_id去查对应的movieid
        elif 8==len(movieid) and '4'==movieid[0:1]:
            if resDict.get(movieid):
                new_movieid=resDict[movieid]['movieid'][3:] #取其movieid的后5位
        else:
            new_movieid='xxx'

        movieidmap_ON[movieid]=new_movieid #映射表,键为旧的movieid，值为新的movieid

    ##获取更新处理后的movied，若更新后的movieid在原来的表中已存在，则修改转换前的movieid为新的movieid
    for mvid in movieidmap_ON.items():
        #if mvid[1] in movieid_O: #如果新的movieid在旧的movieid中存在,
        '''
        不应该是存在才更新，二是对所有的进行更新
        '''
        sql="update mid_table1 set movieid='%s' where movieid='%s'" %(mvid[1],mvid[0])
        cur.execute(sql.encode('utf8'))
        conn.commit()



    #填充中间表2的数据
    sql='select movieid,title,sum(uv),sum(pv) from mid_table1 group by movieid order by uv desc'
    cur.execute(sql.encode('utf8'))
    conn.commit()
    midresults=cur.fetchall()
    if(len(midresults)!=0):
        '''
        mutisql="insert into mid_table2 values('%s','%s','%s','%s')"
        try:
            cur.executemany(mutisql,midresults)
            conn.commit()
        except Exception,e:
            print(e)
        '''
        for item in midresults:
            sql="insert into mid_table2 values('%s','%s','%s','%s')" %(item[0],item[1],item[2],item[3])
            cur.execute(sql.encode('utf8'))
            conn.commit()
    else:
        print('=============mid_table2 is empty==============')

#结果入库
'''
组装后的results结果如下：
[
  [movieid,title,pv,uv,type,title]
   ,
  [movieid,title,pv,uv,type,title]
]
title可以来自src_table,也可以是根据movieid进行查找得到
'''
def mergeResult(conn,cur,stadate):
    sql='select * from mid_table2'
    cur.execute(sql.encode('utf8'))
    conn.commit()
    res=cur.fetchall()
    results=[]
    for index,item in enumerate(res):
        movieid=item[0]
        title=item[1].decode('utf8')  #title可能为空
        if title=="":
            title='Unknown'
        uv=item[2]
        pv=item[3]
        results.append([movieid,title,uv,pv])
        #results.append(list(item))
        mtype,mtitle=getTypeTitle(movieid) #movieid获取影片的类型和名字信息
        '''
        mtype=item[4]
        mtitle=item[5]
        '''
        results[index].append(mtype)
        #results[index].append(mtitle) #item[5]没有使用,title重复


    #将 mdate | movieid |mtype | mtitle | uv | pv  数据先插入到中间结果表xmp_day_play_mid中
    if len(results)!=0:
        for iteml in results:
            sql="insert into xmp_day_play_mid values('%s','%s','%s','%s','%s','%s')" %(stadate,iteml[0],iteml[4],title,iteml[2],iteml[3])  #problem?
            print(sql)
            cur.execute(sql.encode('utf8'))
            conn.commit()
    else:
        print('=============xmp_mid_table is empty==============')

    #将中间结果表xmp_day_play_mid中的数据按uv排序后存入结果表xmp_day_play中
    typelist=('tv', 'movie','anime','teleplay')
    for item in typelist:
        sql='set@x=0'
        cur.execute(sql)
        conn.commit()
        sql='select *,@x:=@x +1 as morder from xmp_day_play_mid where mtype="%s" order by uv desc' %(item)
        cur.execute(sql.encode('utf8'))
        conn.commit()
        results=cur.fetchall()  #取出的结果的类型
        if(len(results)!=0):
            '''
            mutisql="insert into xmp_day_play values('%s','%s','%s','%s','%s','%s','%s')"
            try:
                cur.executemany(mutisql,results)
                conn.commit()
            except Exception,e:
                print(e)
            '''
            for item in results:
                sql="insert into xmp_day_play values('%s','%s','%s','%s','%s','%s','%s')" %(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
                cur.execute(sql.encode('utf8'))
                conn.commit()
        else:
            print('=============xmp_day_play is empty==============')


'''
  后续处理：删除中间表
'''
def dropPro(conn,cur):
    #cur.execute('drop table if exists src_table')
    cur.execute('drop table if exists mid_table1')
    cur.execute('drop table if exists mid_table2')
    cur.execute('drop table if exists xmp_day_play_mid')
    #cur.execute('drop table if exists xmp_day_play')
    conn.commit()

###########################  Process Flow ##########################
if __name__ == "__main__":
    if len(sys.argv)<2:
        stadate='20150817' #raw_input('Please input the stadate:')
    else:
        stadate=sys.argv[1]

    ##建立连接
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hive',db='test') #新建的数据库
    if not conn.open:
        print('open %s db fail'%('test'))
        exit()
    cur=conn.cursor()
    cur.execute('set names utf8')

    ## 初始化表格
    dropPro(conn,cur)  #对可能存在的中间表进行删除处理
    initTable(conn,cur)

    ## 数据准备
    #readData(conn,cur,stadate)

    ## 中间数据处理
    dataMidPro(conn,cur)

    ## 查询结果组装
    mergeResult(conn,cur,stadate)

    ## 删除中间表
    dropPro(conn,cur)

    cur.close()
    conn.close()
