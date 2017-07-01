#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:全局计算库
	Ref:
	State：
	Date:2017/7/1
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


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


# 测试入口
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

