#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:统计公共库
	Ref:
	State：持续更新中
	Date:2017/5/2
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
from pylab import mpl		# 中文设置问题
from collections import defaultdict,OrderedDict


'''
	统计区间部分，并绘制饼图
	Ref:http://blog.sina.com.cn/s/blog_4facccc0010198jz.html
	State：初版完成，增强版要完成区间的自动分割
'''
class DurStatDrawPie():
	def __init__(self):
		self.dur = defaultdict(int)
		self.durdict=OrderedDict()

	# 区间分割
	def _durseg(self,breaks=[1,2,5,10,50]):
		for pos,seg in enumerate(breaks):
			if pos!=len(breaks)-1:
				key="[{start}~{end})".format(start=seg,end=breaks[pos+1])
				self.durdict[key]=(seg,breaks[pos+1])
			else:
				key="[{start}~+)".format(start=seg)
				self.durdict[key]=(seg,max(breaks))
		print self.durdict

	# 区间统计增强版
	def durstat_impl(self):
		with open('../../data/dur_stat.data', 'r') as f:
			for line in f:
				line = line.strip().split()
				num = int(line[0])
				#此处的条件判断该如何完善

	# 区间统计
	def durstat(self):
		with open('../../data/dur_stat.data', 'r') as f:
			for line in f:
				line = line.strip().split()
				num = int(line[0])
				if 1 <= num < 2:
					self.dur["[1~2)"]+=1
				elif 2<=num<5:
					self.dur["[2~5)"]+=1
				elif 5<=num<10:
					self.dur["[5,10)"]+=1
				elif 10<=num<50:
					self.dur["[10,50)"]+=1
				elif 50<=num:
					self.dur["[50,+)"]+=1
				else:
					print 'nodur',num

	# 绘制饼图
	def drawpie(self):
		plt.figure()
		labels = self.dur.keys()
		sizes = self.dur.values()
		#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
		#plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90, pctdistance=0.6)
		plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90, pctdistance=0.6)
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		mpl.rcParams['font.sans-serif'] = ['SimHei']
		mpl.rcParams['axes.unicode_minus'] = False
		plt.title('标题')
		plt.show()
		#plt.savefig("sewe.png") #保存图像

'''
    数据统计
'''
class CPyStat():
    def __init__(self):
        pass

    # 实现groupby,(此处指sum)
    def groupby(self):
         with open(self.src_data,'r') as f:
            for line in f:
                pos,pv,uv=line.strip('\n').split()
                if self.posnum.has_key(pos):
                    self.posnum[pos][1]+=int(pv)
                    self.posnum[pos][2]+=int(uv)
                else:
                    self.posnum[pos]=[int(pv),int(uv)]

# 测试入口
if __name__ == "__main__":
	mc=DurStatDrawPie()
	mc._durseg()
	sys.exit()
	mc.durstat()
	mc.drawpie()

