#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：二分查找与庄家博弈
'''

import sys
import re

all=range(1,101) # 查找范围[1,100]

# 闲家按二分查找依次查找庄家设定的值
def search2(a,m):
    low,high = 1,len(a)-1  # 查找边界
    pay=0
    findtime=1;
    while(low <= high):
        midpos = (low + high)/2
        midval = a[midpos]
        print low,midval,high

        if midval < m:
            low = midpos + 1
            pay+=midval
            findtime+=1
        elif midval > m:
            high = midpos - 1
            pay+=midval
            findtime+=1
        else:
            print "we get:"+str(m)+" we pay:"+str(pay)+"\nwe find in pos:"+str(midpos)+' we find times:'+str(findtime)
            return  midpos;

'''
    闲家策略：找出闲家首猜数
'''
# 闲家博弈:
# 在all中首猜guessv找到setv的次数和路径
def xianboyi(firstguessv,setv):
    times,pay=0,0
    lowpos,highpos=0,len(all)-1  # 默认的高低界
    guessv=firstguessv
    while(lowpos<highpos):
        if guessv<setv:
            lowpos=all.index(firstguessv)
            pay+=guessv
            times+=1
        elif guessv>setv:
            highpos=all.index(firstguessv)
            pay+=guessv
            times+=1
        else:
             print "we get:"+str(setv)+"\nwe pay:"+str(pay)+"\nwe find times:"+str(times)
             return times,pay
        midpos=(lowpos+highpos)/2
        guessv=all[midpos]

# 闲家概率
def xianPlayer():
    for forstguessv in list(range(1,101)):
        for setv in list(range(1,101)):
            times,pay=xianboyi(forstguessv,setv)
            print "首测数\t设置数\t付出\t盈余"
            print forstguessv,"\t",setv,"\t",pay,"\t",400-pay


'''
    庄家策略：找出庄家首设数
'''
# 庄家博弈
def mainboyi():
    pass

# 庄家概率
def mainPlayer():
    for setv in range(1,101):
        pass


if __name__ == "__main__":
    xianPlayer()

