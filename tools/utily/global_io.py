#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:全局IO库
	Ref:
	State：
	Date:2017/7/1
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


###################### file format convert ########################
'''
    txt-->xls
'''
import xlwt
class CTxt2Xls():
    def __init__(self,input):
        self.input=input
        self.output=os.path.splitext(input)[0]+'.xls'
        self.workbook=xlwt.Workbook()

    # 设置输出
    def setoutput(self,output):
        self.output=output

    # 添加图片
    def addpic(self):
        table=self.workbook.add_sheet('T1')
        title="合并标题".decode('utf8')
        rdata=range(1,10)
        table.write_merge(0,1,0,1,title)
        table.write(3,0,'hahh')
        table.insert_bitmap('../data/test.bmp',5,1,4,4,0.5,0.5)

    # 添加文本
    def addtxt(self):
        table=self.data.add_sheet('T2')
        f=open(self.input,'r')
        contents=f.read().decode('utf8').split('\n')
        #contents=f.readlines()
        for i,v in enumerate(contents):
            lcontent=v.strip().split('\t')
            for j,vv in enumerate(lcontent):
                if isinstance(vv,float):
                    table.write(i,j,vv)  #浮点数据可以以指定格式写入
                else:
                    table.write(i,j,vv)
        f.close()

    # 程序入口
    def txt2xls(self):
        self.addtxt()
        self.workbook.save(self.output)


# txt文件转换成xls
def txt2xls(inputfile):
	#Excel
	data=xlwt.Workbook()
	table=data.add_sheet('T1')

	f=open(inputfile,'r')
	contents=f.read().decode('utf8').split('\n')
	#contents=f.readlines()
	for i,v in enumerate(contents):
		lcontent=v.strip().split('\t')
		for j,vv in enumerate(lcontent):
			if isinstance(vv,float):
				table.write(i,j,vv)
			else:
				table.write(i,j,vv)
	f.close()
	outputexcel=os.path.splitext(inputfile)[0]+'.xls'
	data.save(outputexcel)


# 字典文件写入行数据
def dict2tbl():
	category_num={'a':1,'b':2,'c':3}
	stat_res='outrow.log'
	fres=open(stat_res,'a+')

	# 写头
	if not os.path.getsize(stat_res):
		colnames=['date']
		colnames.extend(category_num.keys())
		sformat="%-10s\t"*(len(colnames)-1)+"%-10s\n"
		title=sformat %tuple(colnames)
		fres.write(title)

	# 写数据
	colvalues=['20170329']
	colvalues.extend(category_num.values())
	sformat="%-10s\t"*(len(colvalues)-1)+"%-10s\n"
	result=sformat  %tuple(colvalues)
	fres.write(result)
	fres.close()


# 测试入口
if __name__ == "__main__":
	dict2tbl()

