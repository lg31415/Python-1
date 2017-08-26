#!/user/bin/env python
#-*-coding:utf-8-*-

import os
import sys
import pprint
import re,time

'''
	文件说明：
	一些公用的模块文件,文件读写，查找和遍历
'''


'''
	文件内容统计
	从文件中查找字符串hello,并统计hello出现的次数
'''
def find_count():
	f1=file("file_a.txt","r")
	count=0;
	for s in f1.readlines():
		if s.findall('hello'):
			pass


'''
	获取脚本名
'''
def getscriptName():
	print "当前脚本名:",os.path.realpath(sys.argv[0])
	print "打包前使用:",os.path.join(os.path.abspath('.'),os.path.basename(__file__))



'''
	文件夹遍历
'''
def walkfile():
	filelist=[]
	path='C:\cygwin64\home\yjm'
	for root,dirs,files in os.walk(path):
		for file in files:
			fullfile=os.path.join(root,file)
			filelist.append(fullfile)

	for f in filelist:
		print(f)


'''
	获取文件名和扩展
'''
def getfileext():
	file="zahng_wewj.txt.jpg.ext"
	res=re.split(r'\.',file)
	ffname_noext=os.path.splitext(file)
	print ''.join(res[:-1])
	print ffname_noext[0]



'''
	文件内容查找和替换
'''
def fileReplace():
	f1=file("file_a.txt","r")
	f2=file("bbb.txt","w")
	for s in f1.readlines():  #特别有分量的语句
		f2.write(s.replace("hello","hi"))
	f1.close()
	f2.close()


'''
	文件读写
	print 函数参考：http://www.pythonclub.org/python-basic/print
	若不想输出换行:print(),后面加个逗号,或者换成sys.stdout.write('swwcx')
'''
def fileRead():
	# 方式1
	try:
		f=open("../../data/file_1x.txt","r")
		line=f.readline()
		while line:
			print(line),
			line=f.readline()
		f.close()
	except:
		print "wrong open file"

	#方式2
	print "open file using with"
	with open(r'../../data/filex_a.txt') as f:
		for line in f:
			print line
	print 'continuing doing something'

def fileWrite():
	if 0:
		mset={1,2,3,4,5}
		f=file('../../data/write.txt','a+')
		#f.write(str(mset))
		f.write('-1\t'+'hahgh'+'hwewe'+'\n')
		f.close()

		f=open('../../data/write.txt','r')
		for line in f:
			print line,
		f.close()

	#列表直接写文件
	a=(('zhang','12','man'),('wang','77','woman'),('li','22','woman'))
	f=file('../../data/write.txt','w')
	list2strw=map(lambda x:'\t'.join(x)+'\n',a)
	f.writelines(list2strw)
	f.close()


'''
	中文文件读写
'''
def fileReadWriteCN():
	with open(r"../../data/write_cn.txt",'r') as f:
		for line in f:
			lres=line.decode('utf8').strip('\t').strip('\n').split("\t")
			print lres[2]



'''
	获取文件属性
'''
def fileProperty():
	filep='../data/write1.txt'
	# 文件大小
	if os.path.isfile(filep):
		fsize=os.path.getsize(filep)
		print fsize
	else:
		print "\033[1;31mError:%s import error!\033[0m"  %filep
	# 文件的创建日期
	t=os.stat(filep)[8]
	fmkdate=time.strftime('%Y%m%d',time.localtime(t))


'''
	同时打开多个文件进行并行操作
	参考：http://blog.csdn.net/lanchunhui/article/details/50130175
'''
def mutifileOper(filename1,filename2,filename3):
	with open(filename1, 'rb') as fp1, open(filename2, 'rb') as fp2, open(filename3, 'rb') as fp3:
		#使用with和单循环
		for i in fp1:
			j = fp2.readline()
			k = fp3.readline()
			print(i, j, k)
		#使用zip函数
		for i, j, k in zip(fp1,fp2,fp3):
			print(i,j,k)


'''
	文件重定向
	参考：http://www.cnblogs.com/clover-toeic/p/5491073.html
'''
def file_redirect():
	savedStdout = sys.stdout  # 保存标准输出流
	with open('out.txt', 'w+') as file:
		sys.stdout = file  # 标准输出重定向至文件
		print 'This message is for file!'

	sys.stdout = savedStdout  # 恢复标准输出流
	print 'This message is for screen!'


if __name__ == '__main__':
	file_redirect()
