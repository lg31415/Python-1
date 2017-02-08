#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：合并列表中的元素
'''
import sys

# 根据指定的条件合并列表中的元素
inlist=[(1,4),(6,10),(14,25),(31,55),(78,243)]
def mergelist_impl(inlist):
     mergel=[]
     mergeing=True     # 默认是合并中
     mergelast=False   # 默认最后一个是不合并的
     mergen=0          # 合并次数
     pos=0             # 最后一次合并发生的起始位置
     try:
        for n in range(0,len(inlist)-1):
            n=pos
            if mergeing:                        #正在合并中
                #print len(inlist)
                n= n-mergen if n-mergen>=0 else 0
                pos=n
            if inlist[n+1][0]-inlist[n][-1]<5:
                mergen+=1
                mdur=(inlist[n][0],inlist[n+1][-1])
                del inlist[n+1]                 #删除被合并第n+1个元素
                inlist[n]=mdur                  #修改第n个元素为合并后的值
                if not mergeing:
                    mergel.append(mdur)
                if n==len(inlist)-2:
                    mergelast=True
            else:
                mergeing=False
                mergen=0
                pos=n+1
                mergel.append(inlist[n])
        if not mergelast:
            mergel.append(inlist[-1])
     except Exception,e:
         s=sys.exc_info()
         print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

     return mergel;
    

def mergelist_origin(inlist):
    mergel=[]
    mergelast=False
    try:
        for n in range(0,len(inlist)-1):
            if inlist[n+1][0]-inlist[n][-1]<5:
                mdur=(inlist[n][0],inlist[n+1][-1])
                mergel.append(mdur)
                if n==len(inlist)-2:
                    mergelast=True
            else:
                mergel.append(inlist[n])
        if not mergelast:                       # 将最后未合并的末尾区间统计进来
            mergel.append(inlist[-1])
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    return mergel;


if __name__ == "__main__":
    print "Inlist:",inlist
    print "OrginMerge:",mergelist_origin(inlist)
    print "ImplMerge:",mergelist_impl(inlist)
