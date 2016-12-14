#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yjm'
'''
  功能注释：全局工具函数库
'''

import os
import sys,re,binascii

##################### preprocess ##########################
def strF2J(ustring):
	'''
	unicode
	'''
	return conv.convert(ustring)
def strQ2B(ustring):
	'''
	unicode
	'''
	rstring = ""
	for uchar in ustring:
		inside_code = ord(uchar)
		if inside_code == 0x3000:
			inside_code = 0x0020
		else:
			inside_code-=0xfee0
		if inside_code<0x0020 or inside_code>0x7e:
			rstring += uchar
		else:
			rstring += unichr(inside_code)
	return rstring
def strB2Q(ustring):
	'''
	unicode
	'''
	rstring = ""
	for uchar in ustring:
		inside_code = ord(uchar)
		if inside_code<0x0020 or inside_code>0x7e:
			rstring += uchar
			continue
		if inside_code == 0x0020:
			inside_code = 0x3000
		else:
			inside_code += 0xfee0
		rstring += unichr(inside_code)
	return rstring
def simplePreprocess(ustring):
	'''
	unicode
	'''
	#lower
	ustring  = ustring.lower()
	#Q2B
	ustring = strQ2B(ustring)
	#F2J
	try:
		ustring = strF2J(ustring)
	except:
		ustring = ustring
	return ustring

####################### ip ###############################
import socket,struct
def ipstr2unit(str):
	return socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])
def ipstr2int(str):
	uint = socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])
	return struct.unpack("i", struct.pack('I', uint))[0]
def ipstr2unitReverse(str):
	return socket.htonl(ipstr2unit(str))
def ipstr2intReverse(str):
	return socket.htonl(ipstr2int(str))
def ipnum2str(ip):
	if ip<0:
		ip = struct.unpack("I", struct.pack('i', ip))[0]
	return socket.inet_ntoa(struct.pack('I',socket.htonl(ip))) 

####################### eff ##############################
def is_cookieid_eff(cookieid):
	'''
	32位16进制字符串
	'''
	return re.match("^[A-Fa-f0-9]{32}$",cookieid) is not None
def is_peerid_eff(peerid):
	'''
	16位
	'''
	return re.match("^[0-9a-za-Z]{16}$",peerid) is not None
def is_cid_eff(cid):
	'''
	40位16进制字符串
	'''
	return re.match("^[0-9a-fa-F]{40}$",cid) is not None

###################### lang judge ########################
def is_cn_char(i):
	return 0x4e00<=ord(i)<0x9fa6
def is_cn_or_en(i):
	o = ord(i)
	return o<128 or 0x4e00<=o<0x9fa6
def isxdigit(s):
	return re.match(r'^[A-Fa-f0-9]{1,}$',s) is not None
def isJapan(s):
	'''
	unicode
	'''
	#return re.search(ur"[\u3040-\u309f]+",unicode(s,"utf-8",'ignore')) is not None or re.search(ur"[\u30a0-\u30ff]+",unicode(s,"utf-8",'ignore')) is not None
	return re.search(ur"[\u3040-\u309f]+",s) is not None or re.search(ur'[\u30a0-\u30ff]+',s) is not None

###################### hex unhex ########################
def hexunhex(s):
	tohex=s
	rest=tohex.encode('hex')
	t=[rest[x:x+2] for x in range(0,len(rest),2)]
	shex='%'+'%'.join(t)
	mres=re.sub(r'%','',shex,0)
	unhex=mres.decode('hex')
	print "Origin:",tohex,"\nHex:",rest,"\nHex%:",shex,"\nUnhex:",unhex

# 输入如	#s="%E9%9A%8B%E5%94%90%E8%8B%B1%E9%9B%84%E4%BC%A0"
def unhex(s):
	mres=re.sub(r'%','',s,0)
	unhex=mres.decode('hex')
	print unhex
	return  unhex


'''
	去除url中的%符号
'''
def uri2hex(s):
	ret = ""
	length = len(s)
	i = 0
	while i < length:
		if s[i] == '%' and i+2 < length and isxdigit(s[i+1:i+2]):
			ret += s[i+1:i+3]
			i += 3
		else:
			ret += binascii.hexlify(s[i])
			i += 1
	return ret

def uri2hex2(s):
	if not s:
		s='%e4%b8%ad%e6%96%87'
	print uri2hex(s) #e4b8ade69687

	#uri中的%符号用\x进行替换
	print s.replace('%','\\x').decode('utf-8')
	#print u'中文'.encode('utf-8').decode('utf-8')

####################### lcs #############################
def lcs_session(stringA,stringB):
	'''
	unicode,最大连续公共子串的长度
	'''
	
	lengthA = len(stringA)
	lengthB = len(stringB)

	distanceMatrix = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]

	for i in range(len(stringA)+1):
		distanceMatrix[i][0]  = 0
	for j in range(len(stringB)+1):
		distanceMatrix[0][j] = 0

	ret = []
	for i in range(1,len(stringA)+1):
		for j in range(1,len(stringB)+1):
			if stringA[i-1] == stringB[j-1]:
				distanceMatrix[i][j] = distanceMatrix[i - 1][j - 1]+1
			else:
				ret.append(max(distanceMatrix[i-1][j], distanceMatrix[i][j-1]))
				distanceMatrix[i][j] = 0
	
	ret.append(distanceMatrix[lengthA][lengthB])
	ret.sort(reverse=True)
	return ret[0]
def lcs(stringA,stringB):
	'''
	unicode,最长公共子串的长度,经典lcs算法
	'''
	
	lengthA = len(stringA)
	lengthB = len(stringB)

	distanceMatrix = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]

	for i in range(len(stringA)+1):
		distanceMatrix[i][0]  = 0
	for j in range(len(stringB)+1):
		distanceMatrix[0][j] = 0

	for i in range(1,len(stringA)+1):
		for j in range(1,len(stringB)+1):
			if stringA[i-1] == stringB[j-1]:
				print stringA[i-1],i-1
				distanceMatrix[i][j] = distanceMatrix[i - 1][j - 1]+1
			else:
				distanceMatrix[i][j] = max(distanceMatrix[i-1][j], distanceMatrix[i][j-1])
	return distanceMatrix[lengthA][lengthB]
def simplify_lcs(stringA,stringB):
	'''
	unicode,lcs算法变种,返回最长公共子串:newStringA,newStringB
	'''

	lengthA = len(stringA)
	lengthB = len(stringB)

	b = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]
	c = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]

	for i in range(1,lengthA+1):
		for j in range(1,lengthB+1):
			if stringA[i-1] == stringB[j-1]:
				c[i][j] = c[i-1][j-1] + 1
				b[i][j] = 1
			elif c[i-1][j]>=c[i][j-1]:
				c[i][j] = c[i-1][j]
				b[i][j] = 0
			else:
				c[i][j] = c[i][j-1]
				b[i][j] = -1

	
	i = lengthA
	j = lengthB

	x_indx = []
	y_indx = []

	while i>0 and j>0:
		if b[i][j] == 1:
			x_indx.append(i-1)
			y_indx.append(j-1)
			i-=1
			j-=1
		elif b[i][j] == 0:
			i-=1
		else:
			j-=1

	newStringA = "" 
	if x_indx != []:
		newStringA = stringA[x_indx[len(x_indx)-1]:x_indx[0]+1]

	newStringB = ""
	if y_indx != []:
		newStringB = stringB[y_indx[len(y_indx)-1]:y_indx[0]+1]


	return newStringA,newStringB

################### similar distance ####################
def editdistance(stringA,stringB):
	'''
	unicode,计算编辑距离
	'''
	lengthA = len(stringA)
	lengthB = len(stringB)

	if lengthA==0 or lengthB==0:
		return sys.maxint
	distanceMatrix = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]
	for i in range(lengthA+1):
		distanceMatrix[i][0]=i
	for j in range(lengthB+1):
		distanceMatrix[0][j]=j
	for i in range(1,lengthA+1):
		for j in range(1,lengthB+1):
			if stringA[i-1]==stringB[j-1]:
				cost=0
			else:
				cost=1
			distanceMatrix[i][j]=min(distanceMatrix[i-1][j]+1,distanceMatrix[i][j-1]+1,distanceMatrix[i-1][j-1]+cost)
	return distanceMatrix[lengthA][lengthB]
def regex_editdistance(stringA,stringB):
	'''
	unicode,计算编辑距离的正在，返回list
	'''
	lengthA = len(stringA)
	lengthB = len(stringB)
	if lengthA==0 or lengthB==0:
		return sys.maxint
	distanceMatrix = [[0 for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]
	pathMatrix = [[ [] for j in range(len(stringB)+1)] for i in range(len(stringA)+1)]
	for i in range(lengthA+1):
		distanceMatrix[i][0]=i
	for j in range(1,lengthB+1):
		distanceMatrix[0][j]=j
	for i in range(1,lengthA+1):
		for j in range(1,lengthB+1):
			if stringA[i-1]==stringB[j-1]:
				distanceMatrix[i][j] = distanceMatrix[i-1][j-1]
				pathMatrix[i][j] = [i-1,j-1]
			else:
				distanceMatrix[i][j] = 1 + min(distanceMatrix[i-1][j],distanceMatrix[i][j-1],distanceMatrix[i-1][j-1])
				if min(distanceMatrix[i - 1][j],distanceMatrix[i - 1][j - 1]) <= distanceMatrix[i][j - 1]:
					x = i-1
				else:
					x = i

				if min(distanceMatrix[i][j - 1 ],distanceMatrix[i - 1][j - 1]) <= distanceMatrix[i - 1][j]:
					y = j-1
				else:
					y = j
			#	x = i-1 if min(distanceMatrix[i - 1][j],distanceMatrix[i - 1][j - 1]) <= distanceMatrix[i][j - 1] else i
			#	y = j-1 if min(distanceMatrix[i][j - 1 ],distanceMatrix[i - 1][j - 1]) <= distanceMatrix[i - 1][j] else j
				pathMatrix[i][j] = [x,y]
	x = lengthA
	y = lengthB

	myx = 0
	myy = 0
	flag = False

#	isStartPattern = False

	sbx = ""
	l = []

	while x>0 and y>0:
		myx = pathMatrix[x][y][0]
		myy = pathMatrix[x][y][1]
		
		if (myx >= lengthA or myy >= lengthB):
			x = myx
			y = myy
#			isStartPattern = True
			continue

#		if isStartPattern == True:
#			# for first (.*?)
#			l.append('(.*?)')
#			isStartPattern = False

		print x,y,myx,myy,stringA[myx],stringB[myy]
		if stringA[myx] == stringB[myy] and myx != x and myy != y:
			sbx+=stringA[myx]
			if not flag: flag = True
		else:
			if flag and len(sbx) >0:
				l.append(sbx[::-1])
				sbx = ""
				flag = False
			if not flag and len(sbx)==0:
				l.append('(.*?)')
				flag = True
		x = myx
		y = myy
	if flag and len(sbx)>0:
		l.append(sbx[::-1])
	
# for last (.*?)
#	if (x>0 or y>0) and l[len(l)-1]!='(.*?)':
#		l.append('(.*?)')
	
	l.reverse()

	return ''.join([item for item in l])

###################### format convert ########################
def txt2xls(inputfile):
	import xlwt
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
	

#######################主测试入口
if __name__ == "__main__":
	#求编辑距离
	stringA = "星光伴我心".decode('utf8')
	stringB = "太极2星球崛起".decode('utf8')
	print editdistance(stringA,stringB)
	print "---------------------------"

	# 正则编辑距离
	regstr = regex_editdistance(stringA,stringB)
	a = re.search(regstr,stringA)
	b = re.search(regstr,stringB)
	print regstr
	print "---------------------------"

	# 最长公共子串
	print lcs(stringA,stringB)
	print lcs_session(stringA,stringB)
	print "---------------------------"

	(a,b) = simplify_lcs(stringA,stringB)
	print a.encode('utf8'),b.encode('utf8')
	print "---------------------------"


	#hex unhex
	tohex='隋唐英雄传'
	s="%E9%9A%8B%E5%94%90%E8%8B%B1%E9%9B%84%E4%BC%A0"
	unhex(s)
	#hexunhex(tohex)




