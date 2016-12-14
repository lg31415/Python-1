#-*-coding:utf-8-*-
'''
	正则表达式的学习：
	详细参考网址：http://wiki.jikexueyuan.com/project/python-crawler-guide/regular-expressions.html#7907ec6cc04be6c7f8cf8ac272215946
'''

import os
import sys
import re

# 正则匹配
def rematch():
	#re.match(r'正则表达式', testtext):  也可以之间这样使用
	regex_expr='.*search.xmp.kankan.com*'  #[a-z]{1,2}[0-9]{1,2}
	to_match_str='xwejtrere%search.xmp.kankan.com%xwrwewrw'
	regex=re.compile(regex_expr)           #输入的字符在a-z之间，且长度为3
	m1=re.match(regex,to_match_str)        #match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。常见的判断方法就是
	if m1 is not None:
		print 'm1 matched'
		print m1.groups(),m1.group(0)
	else:
		print 'm1 is not matched'

# 正则搜索
def research():
	regex=re.compile('\(?0\d{2}[)-]?\d{8}')
	m4=re.search(regex,'022-12345678 (010)88888882 02344445555') #找到第一个就返回,返回的是一个对象
	#print m4  #返回的是找到的对象的地址，要用下面的group进行解析一下
	if m4 is not None:
		print m4.group()  #注意到group(0)永远是原始字符串，group(1)、group(2)……表示第1、2、……个子串。
		print type(m4.group(0))

	regex_n=re.compile(r'\d{1,}')
	rm4=re.search(regex_n,'d123ewrewe3');
	if rm4:
		print rm4.group()


	m5=re.findall(regex,'(010)88888882 022-12345678 02344445555') #返回的直接是所有找到的结果
	#print m5
	#列表解析
	sum([int(x) for x in m5])
	print type(m5)

# 正则查找
def refindall():
	res=re.findall(r'\d+','n232owe23r22343')  #以列表形式返回查找到的全部子串
	print res

	resiter=re.finditer(r'\d+','n232owe23r22343') # 以迭代器的形式返回所需要的结果
	for it in resiter:
		print it.group()

# 正则索引
def reindex():
	m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world! sign')
	print "m.string:", m.string
	print "m.re:", m.re
	print "m.pos:", m.pos
	print "m.endpos:", m.endpos
	print "m.lastindex:", m.lastindex
	print "m.lastgroup:", m.lastgroup
	print "m.group(1,2):", m.group(1, 2)
	print "m.groups():", m.groups()
	print "m.groupdict():", m.groupdict()
	print "m.start(2):", m.start(2)
	print "m.end(2):", m.end(2)
	print "m.span(2):", m.span(2)
	print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')

# 正则分割（对多个分割符存在的情况下）
def resplit():
	mlist=re.split(r':|,','today:12:23,32,Fri') # 返回的是一个匹配的列表
	print mlist

# 正则替换
def resub():
	str1='hwe12,we hwe1224,hwe232'
	mres=re.sub(r'hwe\d{2}','hello',str1,0) #返回被替换后的字符串,最后一个参数表示替换的次数
	print mres

	mres,mcnt=re.subn(r'hwe\d{2}','hello',str1,2) #mcnt是被替换的次数，mres是替换后的字符串
	print mres,mcnt

	#另外的写法
	repx=re.compile('hwe')
	print repx.sub('word',str1)




if __name__=="__main__":
	#rematch()
	#research()
	#refindall()
	reindex()
	#resplit()
	#resub()