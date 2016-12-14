#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python操作Excel
           利用到xlrd和xlwt库
  参考链接：http://www.cnblogs.com/lhj588/archive/2012/01/06/2314181.html
'''

import xlrd
import xlwt
import sys
import MySQLdb

'''
	xls read & write
'''
#xls的读
def mxlsread():
    data=xlrd.open_workbook("../data/mxls.xlsx")
    table=data.sheets()[0]
    nrows=table.nrows
    ncols=table.ncols
    for i in range(nrows):
        for item in table.row_values(i):
            if isinstance(item,float):
                print item,
            else:
                print item.encode('utf8'),
        print

#xls的写
def mxlswrite():
    data=xlwt.Workbook()  #创建一个工作簿
    table=data.add_sheet('T1')   #创建一个工作表
    table.write(0,0,'hah')
    data.save('../data/test.xls')



'''
	MySQL<->Excel
'''
# 读取mysql的数据并保持成excel文件
def msql2xls():
    #mysql
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='task')
        if  not conn.open:
            print('Error Open')
        else:
            print('conn has sucessfuly open')
    except Exception,e:
        print(e.args[0],e.args[1])
        sys.exit()
    cur=conn.cursor()
    sql="select * from customers;"
    cur.execute(sql)
    alldata=cur.fetchall()
    print('type<fetchall>',type(alldata),alldata)
    if 0==len(alldata):
        print('error happen')
        exit()
    #Excel
    data=xlwt.Workbook()                  #创建一个工作簿
    table=data.add_sheet('ResutlTable')   #创建一个工作表
    for i,v in enumerate(alldata):        #下面的i和j用来获取单元格的位置
        for j,vv in enumerate(v):
            table.write(i,j,vv)
    data.save('../data/sqlxls.xls')


'''
	txt<->xls
'''
#从格式化txt文件读取数据转为xls
def mtxt2xls():
    #Excel
    data=xlwt.Workbook()         #创建一个工作簿
    table=data.add_sheet('T1')   #创建一个工作表

    f=open("../data/xlstxt.txt",'r')
    contents=f.read().decode('utf8').split('\n')
    #contents=f.readlines()
    for i,v in enumerate(contents):
        lcontent=v.strip().split('\t')
        for j,vv in enumerate(lcontent):
            if isinstance(vv,float):
                table.write(i,j,vv)
            else:
                table.write(i,j,vv)
    data.save('../data/txtxls.xls')

# 向xls中插入图片
def xlsaddpic():
    #Excel
    data=xlwt.Workbook()
    table=data.add_sheet('T1')

    title="合并标题".decode('utf8')
    rdata=range(1,10)
    table.write_merge(0,1,0,1,title)
    table.write(3,0,'hahh')
    table.insert_bitmap('../data/test.bmp',5,1,4,4,0.5,0.5)

    data.save('test.xls')


'''
	csv<->xls
'''
#csv文件的写入（生成）
import csv
import codecs
def mcsvwrite():
    csvfile=file('../data/csv_write.csv','wb')
    csvfile.write(codecs.BOM_UTF8) #解决中文乱码问题
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['姓名', '年龄', '电话'])  #写入列名
    # 注意写入的是字典数据
    data = [
    ('小河', '25', '1234567'),
    ('小芳', '18', '789456')
    ]
    csvwriter.writerows(data)
    csvfile.close()

#读取csv文件
def mcsvread():
    csvfile=file('../data/csv_write.csv','rb')
    csvreader=csv.reader(csvfile)
    print 'type(csvreader):',type(csvreader)
    for row,line in enumerate(csvreader):
        print row,line  #line是一个列表
        for field in line:
            print '-',field
    csvfile.close()




if __name__ == "__main__":
    #mxlsread()
    #mxlswrite()
    #msql2xls()
    #mtxt2xls()
    mcsvwrite()
    mcsvread()



