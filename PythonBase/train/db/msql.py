# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：数据库操纵
  source: http://www.cnblogs.com/edisonfeng/p/3205707.html
'''
# import  pymysql
#
# conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root')
# cur=conn.cursor()
# conn.select_db('peerid_db')
#
# values=[]
# for i in range(20):
#     values.append((i,'hi rollen'+str(i)))
# print(values)
#
# mvalues=('niahao','hallo',1)
# sql="insert into xmp_days_source(sta_date,sta_source,install_num) values(%s,%s,%d)" % mvalues
# print(type(sql))
# print(sql)
# cur.execute(sql)
# conn.commit()
# cur.close()
# conn.close()



import os,sys,string
import pymysql
import MySQLdb

try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='mjoin')
    #对打开是否成功的测试
    if  not conn.open:
        print('Error Open')
    else:
        print('conn has sucessfuly open')
except Exception,e:
    print(e.args[0],e.args[1])
    sys.exit()

cur=conn.cursor()


# Insert Data
def insertSingle():
    #sql="insert into persons(Id_P,LastName) VALUES (%d,'%s')" % (9,'yjm')  #按原始类型的标准插入
    sql="insert into persons(Id_P,LastName) VALUES (%s,'%s')" % (16,'yjm')  #按转换类型插入,整型当成字符型输入
    #sql="insert into persons(Id_P,LastName) VALUES ('%s','%s')" % (27,'this is a test')  #按转换类型插入,整型当成字符型输入,但是插入指定的时候添加了引号,但依然插入正确
    print(sql)
    try:
        cur.execute(sql)
        #conn.commit()
    except Exception,e:
        print e

#Insert Muti Data
def insertMuti():
    sql="insert into persons(Id_P,LastName) VALUES (%s,%s)"
    print(sql)
    mutivals=((int(11),"zhag"),(int(12),"gaug"))
    try:
        cur.executemany(sql, mutivals)
    except Exception,e:
        print('Fail to insert values',e)


#Select Data
'''
  一次性取出全部数据：原来是什么类型的数据，取出来也是什么类型的数据
'''
def selectManyData(conn,cur):
    #测试1
    sql="select Id_P,LastName from persons ORDER BY Id_P"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    alldata=cur.fetchall()
    print('type<fetchall>',type(alldata),alldata)
    if alldata: #读取到数据
        for rec in alldata:
            print(type(rec[0]),rec[0],type(rec[1]),rec[1])
    conn.commit()

    #测试2
    sql="select Id_P,LastName from persons ORDER BY Id_P"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    manydata=cur.fetchmany(3)
    print('type<fetchall>',type(manydata),manydata)
    if manydata: #读取到数据
        for rec in manydata:
            print(type(rec[0]),rec[0],type(rec[1]),rec[1])
    conn.commit()

    # 测试3（带字段名读取）(参考：http://python.jobbole.com/85589/)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("select * from persons limit 3")
    res=cur.fetchall()
    print res


'''
  逐个取数据：
'''
def selectEachData():
    if None:
        sql="use mjoin;select Id_P,LastName from persons ORDER BY Id_P"
        try:
            cur.execute(sql)
        except Exception,e:
            print(e)
        onedata=cur.fetchone()
        print('type<fetchall>',type(onedata),onedata)
        while onedata: #读取到数据
            for rec in onedata:
                print rec,
            print
            onedata=cur.fetchone()
        #conn.commit()

    ## 测试2
    sql="select gender from datatype where id=2;"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    onedata=cur.fetchone()
    print type(onedata),onedata['gender']
    conn.commit()


#test excute和commit的功能
def testExcuteAndCommit():
    try:
        affrows=cur.execute("select * from persons where LastName='%s'",("Bush"))
        conn.commit()
        if not affrows:
            results=cur.fetchone()
            print results
            for item in results:
                print item
    except Exception,e:
        print e

def closeConn():
    cur.close()
    conn.close()



if __name__ == "__main__":
    #insertSingle()
    testExcuteAndCommit()
    #selectManyData(conn,cur)
    #selectEachData()
    #closeConn()
    #mysqlvisual(conn,cur)




