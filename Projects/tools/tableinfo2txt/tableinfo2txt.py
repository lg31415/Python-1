#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：取得数据库中所有表的字段信息，输出到txt文件
  升级：后续改进生xls文档
  时间：2015年10月15日19:34:36
'''

import pymysql
import os,sys

'''
    获取数据库连接
'''
def openDB(dbname):
    try:
        conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db=dbname)
        #对打开是否成功的测试
        if  not conn.open:
            print('Error Open')
        else:
            print('Conn has sucessfuly open')
    except Exception,e:
        print(e.args[0],e.args[1])
        sys.exit()
    cur=conn.cursor()
    return conn,cur

'''
    获取所有表的所有字段（利用命令行调用）
'''
def getTablesFields(conn,cur,dbname):
    sql="select concat('desc ',table_name) from information_schema.tables where table_schema='%s'" %dbname
    cur.execute(sql)
    ret=cur.fetchall()
    if ret:
        for esql in ret:
            #cur.excute(esql)
            os.system("echo.  >>result.txt")
            cmd="echo %s>>result.txt" %esql[0].split()[1]
            os.system("echo ----------------------------------------- >>result.txt")
            print cmd
            os.system(cmd)
            sql='mysql -uroot -proot %s -e "%s">>result.txt' %(dbname,esql[0])
            os.system("echo ======================================== >>result.txt")

            print sql
            os.system(sql)
    conn.commit()


'''
    改进版想实现的是日志重定向，通过那个功能实现
    暂未实现（2015年10月20日）
'''
def getTablesFields_Imp(conn,cur,dbname):
    cur.execute("\\T  D:\\result.txt")  #关键是这一句如何通过程序实现
    sql="select concat('desc ',table_name) from information_schema.tables where table_schema='%s'" %dbname
    cur.execute(sql)
    ret=cur.fetchall()
    if ret:
        for esql in ret:
            cur.execute(esql[0])
    conn.commit()



if __name__ == "__main__":
    dbname='task'
    conn,cur=openDB(dbname)
    getTablesFields(conn,cur,dbname)

