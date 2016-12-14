# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：播放排行统计
'''

import pymysql
import json
import urllib2


#########################  Methods ##################################

#kankan_dict:由kankan_id反解析movieid
'''
[{"type":"anime","movieid":"mi1000004","kankan_id":"60242"},....,{"type":"movie","movieid":"mi1000006","kankan_id":"63673"}]
由kankan_id反解析movieid
'''
url='http://media.v.xunlei.com/pc/id_mapping?media_type=|tv|anime|teleplay|movie'
def urlParase(url):
    resDict={}
    resonse=urllib2.urlopen(url)
    content=resonse.read()
    plist=json.loads(content) #解析后得到的列表，先转换一下
    for item in plist:
        kankan_id=item['kankan_id']
        if kankan_id!="":
            resDict[kankan_id]={'type':item['type'],'movieid':item['movieid']}
    print resDict
    return resDict

urlParase(url)


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
    resonse=urllib2.urlopen(url)
    content=resonse.read()
    pdict=json.loads(content) #解析后得到的字典
    type=pdict.get['type']
    title=pdict.get['title']
    return type,title


###########################  Process Flow ##########################

##建立连接
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='task3') #新建的数据库
if conn==0:
    print('open %s db fail'%('task2'))
    exit()
cur=conn.cursor()

##创建原始表(src_table)
'''
fpeerid | fmovieid | ftitle
'''
sql='create table if not exists src_table(fpeerid varchar(10),fmovieid varchar(10),ftitle varchar(30) character set utf8'
cur.execute(sql)
conn.commit()

#导入数据
load_sql="load data local infile '%s' into table '%s'" %('file.txt','src_table') #20150817当天数据载入
cur.execute(load_sql)
conn.commit()

##数据分析(创建中间表mid_table1)
'''
movieid | title  |   pv |  uv
'''
sql='create table if not exists mid_table1 select fmovieid as movieid,ftitle as title,count(*) as pv,count(distinct fpeerid) as uv from src_table group by fpeerid order by uv desc'
cur.execute(sql)
conn.commit()


#从中间表取movieid进行分析
sql='select movieid from mid_table1'
cur.execute(sql)
conn.commit()
movieid_O=cur.fetchall() #返回的是旧的movieid的元组


##对movieid进行转化处理分析,配对修改
movieidmap_ON={}          #旧新movieid对照字典
resDict=urlParase(url)
for items in movieid_O:  #取查询结果进行分析
    movieid=items[0]
    if 7==len(movieid):
        new_movieid='mi'+movieid
    elif len(movieid)==5:
        new_movieid=resDict[movieid]['movieid']  #把item作为kankan_id去查对应的movieid
    elif 8==len(movieid) and '4'==movieid[0:1]:
        if resDict.get(movieid):
            new_movieid=resDict[movieid]['movieid'][3:] #取其movieid的后5位
    else:
        new_movieid="xxx"

    movieidmap_ON[new_movieid]=movieid #映射表

##获取更新处理后的movied，若更新后的movieid在原来的表中已存在，则修改转换前的movieid为新的movieid
for mvid in movieidmap_ON.items():
    if mvid[0] in movieid_O:
        sql='update mid_table1 set movieid=%s where movieid=%s ' %(mvid[0],mvid[1])
        cur.execute(sql)
        conn.commit()


##将着两个movieid的数据进行合并，主要是uv和pv数据
#创建中间表mid_table2,
'''
   movieid |  title | pv | uv
'''
sql='create table if not exists mid_table2 select movieid,title,sum(pv),sum(uv) from mid_table1 group by peerid order by uv desc'
cur.execute(sql)
conn.commit()
res=cur.fetchall()

#查询结果组装
results=[]
i=0
for item in res:
    movieid=item[0]
    title=item[1]
    pv=item[2]
    uv=item[3]
    results[i]=[movieid,title,pv,uv]

    type,title=getTypeTitle(movieid) #movieid获取影片的类型和名字信息
    results[i].append(type)
    results[i].append(title)
    i=i+1


##最后将影片的信息综合总统计结果
'''
日期   影片id   影片类型  影片名  日用户访问 日浏览访问 日访问排名
mdate | movieid | mtype |  mtype | uv     |    pv    | morder
'''
sql='create table if not exists xmp_day_play_mid(mdate date,movieid varchar(10),mtype varchar(10),mtitle varchar(30),uv int(10),pv int(10),morder int(5)) character set utf8'
cur.execute(sql)
conn.commit()

#将 mdate | movieid | mtype | mtype | uv | pv 数据先插入到表xmp_day_play_mid中
for item in results:
    sql='insert into xmp_day_play_mid values(%s,%s,%s,%s,%d,%d)' %('20150817',item)
    cur.execute(sql)
    conn.commit()

#查询更新，计算排名(在使用变量的时候，不要使用分组),查询结果暂存在视图mid_view
typelist=('tv', 'movie','anime','teleplay')

#将mid_view中的数据按uv排序后存入xmp_day_play的结果表中
for item in typelist:
    sql='set@x=0;create view if not exists xmp_day_play select *,@x:=@x +1 as morder from xmp_day_play_mid where mtype="%s" order by uv desc' %(item)
    cur.execute(sql)
    conn.commit()


#按日期排序
sql='create table if not exists xmp_day_play select * from xmp_day_play group by mdate'
cur.execute(sql)
conn.commit()

#后续处理
sql='''
drop table src_table;
drop table mid_table1;
drop table mid_table2;
drop table xmp_day_play_mid;
drop view  xmp_day_play;
'''
cur.execute(sql)
conn.commit()

cur.close()
conn.close()


if __name__ == "__main__":
    pass
