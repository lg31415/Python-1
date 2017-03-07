#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：redis数据库使用
  参考：http://www.cnblogs.com/melonjiang/p/5342505.html
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import redis
import MySQLdb
import random


# mysql
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='snh48') #新建的数据库
    cur=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute('set names utf8')
except Exception,e:
    print('open %s db fail'%('snh48'))
    sys.exit()

'''
    从redis中取数据
'''
def mredis():
    r=redis.StrictRedis(host='localhost',port=6379)
    r.flushdb()    #清空所有数据
    for i in (10,30,40,50):
        r.zadd("key"+str(i),
               random.randrange(40,50),1488874454+random.randrange(i,i+10),
               random.randrange(40,60),1488874454+random.randrange(i+10,i+20),
               random.randrange(50,70),1488874454+random.randrange(i+30,i+40))

    r.save()

    f=open('redis_export.txt','w')
    for i in (10,20,30,40,50):
        print ">>>>>>>>>>>>>>key"+str(i)
        aa=r.zrangebylex("key"+str(i),"[1488874464","[1488874584")
        print aa
        for t in aa:
            print t+":",r.zscore("key"+str(i),t)
            print r.zrangebyscore("key"+str(i),50,60)
            info='\t'.join(["key"+str(i),t,str(r.zscore("key"+str(i),t))])+"\n"
            f.write(info)

            # 采用逐条插入的方式
            #insert_sql="insert into task1_tbl(s_key,t_time,vv) VALUES ('%s','%s','%s')" %("key"+str(i),t,r.zscore("key"+str(i),t))
            #print insert_sql
            #cur.execute(insert_sql)

    f.close()

    #采用文件加载的方式
    cur.execute("delete from task1_tbl;")
    load_sql="load data local infile '%s' into table task1_tbl(s_key,t_time,vv);" %('redis_export.txt')  #fields terminated by '\t'
    print load_sql
    cur.execute(load_sql)
    conn.commit()




'''
    同步redis数据到mysql的建表准备
'''
def rsync_to_mysql():
    sql='CREATE TABLE if not EXISTS (id  bigint(20) NOT NULL , ' \
        's_key  varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL ,' \
        ' t_time  bigint(20) NOT NULL ,' \
        ' vv  int(255) UNSIGNED ZEROFILL NULL DEFAULT NULL ,' \
        ' PRIMARY KEY (id),' \
        ' UNIQUE INDEX s_key (s_key) USING BTREE ,' \
        'INDEX t_time (t_time) USING BTREE )' \
        'ENGINE=InnoDB' \
        ' DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci' \
        ' ROW_FORMAT=COMPACT ;'

    cur.execute(sql)
    conn.commit()


'''
    同步mysql数据到redis
'''
def rsync_to_redis():
    pass



'''
    从mysql数据统计排行
'''
def stat_rank():
    this_start=0
    this_end=0
    last_start=0
    last_end=0

    this_sql="select s_key,sum(vv) as cnt from task1_tbl where t_time>%s and t_time<%s group by s_ley order by cnt desc;" %(this_start,this_end)
    last_sql="select s_key,sum(vv) as cnt from task1_tbl where t_time>%s and t_time<%s group by s_ley order by cnt desc;" %(last_start,last_end)
    whatis=" a.s_key as '人物',a.cnt as '排行' ,a.cnt-b.cnt as '升降' "     #如何添加排行（前端处理吧）
    sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on a.s_key=b.s_key order by a.cnt desc".format(whatis=whatis,tablea=this_sql,tableb=last_sql)
    print sql
    cur.execute(sql)
    conn.commit()


if __name__ == "__main__":
    mredis()
