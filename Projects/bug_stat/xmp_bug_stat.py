#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:xmp bug数据统计
	Ref:http://blog.csdn.net/yueguanghaidao/article/details/7265246
	State：完成（2017年1月4日）
	Date:2016/12/27
	Author:tuling56
'''
import re, os, sys

from datetime import date, datetime, timedelta
import zipfile
from xml.etree import ElementTree
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

src_root_path="/data4/xmp_bug_data"

file_path=os.getcwd()
data_path=file_path.replace("/bin","/data")

if len(sys.argv) <= 2:
	calcday_date = date.today() - timedelta(days=1)
	calcday = calcday_date.strftime("%Y%m%d")
	src_path= os.path.join(src_root_path,calcday_date.strftime('%Y-%m-%d'))
elif len(sys.argv) == 3:
	calcday = sys.argv[1]
	src_path= sys.argv[2]

loaddata= os.path.join(data_path,"bug_stat_"+calcday)


print "\033[1;31msrc_path:\033[0m",src_path
print "\033[1;31mload_data:\033[0m",loaddata


'''
	解析汇总文件
	输入：bug汇总总文件
'''
def parse_total():
	bug_files={}
	data_total=os.path.join(src_path,'stat.txt')
	with open(data_total,'r') as f:
		for line in f:
			date,flag,xmp_version,err_count=line.strip().split('|')
			try:
				date=date.split(":")[1].strip()
				code_addr=err_count.split(',')[0].strip()
				count=err_count.split(':')[1].strip()
			except Exception,e:
				print "\033[1;31mParseError:\033[0m:",str(e)
			bug_file=os.path.join(xmp_version,code_addr+".zip")
			bug_files[bug_file]=[calcday,xmp_version,code_addr,count]
	print "bug汇总文件解析完成"
	return  bug_files



'''
	bug解析系统
	输入：zip封装的bug文件
'''
class BugStat():
	def __init__(self,bugfile):
		self.bug_file=bugfile
		self.xmlcontent=""
		self.bug_dict={}

	'''
		解析zip文件内容
	'''
	def extract_zip(self):
		zipFile = zipfile.ZipFile(os.path.join(src_path,self.bug_file))
		try:
			bugdata = zipFile.read('BugReport.xml')
			self.xmlcontent=bugdata
		except Exception,e:
			print "\033[1;31mZipError:\033[0m:",str(e)
			print "\033[1;31mProblemFile:\033[0m",os.path.join(src_path,self.bug_file)
			return ""
		finally:
			zipFile.close()

		return 1

	'''
		解析xml文件，构造bug字典
	'''
	def extract_xml(self):
		if self.xmlcontent:
			root = ElementTree.fromstring(self.xmlcontent)
		else:
			return ""

		# 获取modulelist(构造模块字典)
		mode_dict={}
		module_node=root.find('ModuleList')
		mode_nodes=module_node.getiterator("Module")
		for mode_node in mode_nodes:
			mode_info=mode_node.attrib
			m_version=mode_info['version'].split('(')[0].strip()
			m_path=mode_info['path']
			m_name=mode_info['name']
			m_baseaddr=eval('0x'+mode_info['baseaddr'])
			m_size=mode_info['size']
			m_endaddr=m_baseaddr+int(m_size)

			issystem=False
			if m_path.find('System32')!=-1 or m_path.find('SysWoW64')!=-1:
				issystem=True
			mode_dict[m_name]={"issystem":issystem,"version":m_version,"addr_dur":[m_baseaddr,m_endaddr]}

		# 获取exceptionlist(构造异常字典，采用迭代的方式)
		exception_node = root.find('Exception')
		code_reason=exception_node.attrib['code']
		stack_nodes=exception_node.getiterator("Frame")
		for stack_node in stack_nodes:
			addr_hex=stack_node.attrib['address']			# 调用崩溃堆栈的地址
			addr=eval('0x'+addr_hex)
			for mode,values in mode_dict.items():
				if(not values['issystem'] and addr>values['addr_dur'][0] and addr<values['addr_dur'][1]):	#该模块的崩溃原因找到
					self.bug_dict[self.bug_file]=[code_reason,mode,values['version']]
					break

		return 1

'''
	结果文件存储(列表存储的常见形式)
'''
def result_write(bug_info):
	with open(loaddata,'w') as f:
		for values in bug_info.values():
			print >>f,'\t'.join(list(map(lambda v:str(v),values)))



'''
	结果文件入库（将结果文件存入mysql）[这部分放在shell里也行，python只负责运算]
'''
def result_staged(calcday,loaddata):
	#csql="use pgv_stat_yingyin;create table if not exists xmp_bug_stat(date varchar(10),version varchar(20),code_addr varchar(50),code_reason varchar(255),module varchar(20),module_version varchar(20),num int)ENGINE=MyISAM DEFAULT CHARSET=utf8;"
	try:
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hive',db='pgv_stat_yingyin')
		cur=conn.cursor()
	except Exception,e:
		print "open connection error:\n",str(e)
		sys.exit()
	
	#cur.execute(csql)
	lsql1="delete from pgv_stat_yingyin.xmp_bug_stat where date='%s';" %(calcday)
	print(lsql1)
	cur.execute(lsql1)
	conn.commit()
	
	lsql2="load data local infile '%s' into table pgv_stat_yingyin.xmp_bug_stat(date,version,code_addr,num,code_reason,module,module_version);" %(loaddata)
	print(lsql2)
	cur.execute(lsql2)
	conn.commit()

	conn.close()




# 程序主入口
if __name__ == "__main__":
	# step1:汇总解析
	bug_info=parse_total()
	# step2:崩溃原因查询
	for key,value in bug_info.items():
		try:
			bgstat=BugStat(key)
			bgstat.extract_zip()
			if bgstat.extract_xml():
				bug_info[key].extend(bgstat.bug_dict[key])
				#print key,bug_info[key]
		except Exception,e:
			print "\033[1;31mZipXmlError\033[0m",str(e)
			
	# step3:结果写入
	result_write(bug_info)
	# step4:结果入库
	result_staged(calcday,loaddata)





