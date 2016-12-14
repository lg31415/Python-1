#!/bin/env/pyhton
#-*-coding:utf8-*-
'''
   功能说明：大文件分拆成多个小文件并导入到xls的工作表
   备注：大文件分拆功能不在这里实现
'''
import xlwt
import sys
import os
import re



class MutiText2XLS(object):
	def __init__(self,datapath):
		self.datapath='.'
		self.filelist=[]
		self.outputexcel='.'

	#获取文件列表
	def getfilelist():
		global filelist
		for root, dirs, files in os.walk(self.datapath):
			for file in files:
				mclass=re.split('\\\\',root)[-1]
				readfile= os.path.join(root, file)
				if readfile.endswith('.txt'):
					self.filelist.append(readfile)
		return filelist

	'''
		将文件列表里的每个文件添加到工作簿的工作表
	'''
	def txt2xls():
		self.getfilelist()
		xlsdata=xlwt.Workbook()
		for inputfile in self.filelist:
			inputname=os.path.split(inputfile)[1] #以文件名作为工作表名
			table=xlsdata.add_sheet(inputname)   

			# 处理每个文件
			with open(inputfile,'r') as f:
				for line in f:		
					contents=f.read().decode('utf8').split('\n')
					for i,v in enumerate(contents):
						lcontent=v.strip().split('\t')
						for j,vv in enumerate(lcontent):
							if isinstance(vv,float):
								table.write(i,j,vv)
							else:
								table.write(i,j,vv)		
		xlsdata.save(self.outputexcel)


if __name__ == '__main__':
	mtxt2xls=MutiText2XLS('./lab',"local_play_20160921.xls")
	mtxt2xls.txt2xls()
