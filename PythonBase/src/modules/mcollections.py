#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：collections模块中几个重要类学习
'''
from  collections import  *

class collectionCT(object):
    def mnametuple(self):
        Point=namedtuple('Point',['x','y'])
        p=Point(1,3)
        print( p.x,p.y)

    def mdeque(self):
        q=deque(['a','b','c'])
        q.append('t')
        q.append('t1')
        q.appendleft('h') #向同头部添加元素
        q.appendleft('h1')

        q.pop()     #弹出队列尾
        q.popleft() #弹出队列头

        print(q)

    def mdefaultdict(self):
        dd=defaultdict(lambda:'noexits')  #在创建的时候直接指定默认字典
        dd['key1']='val1'
        print dd['key2'] # 返回默认值(这个的权限最高)

        #
        dd_new={}
        if 'key2' not in dd_new:
            dd_new.setdefault('key2',{'k':'v'}) #字典设置默认值
        print dd_new['key2']
        #print dd_new['key1']
        print dd_new.get('key1','nononono')

        #默认字典实现计数
        dc=defaultdict(int)
        for k in 'xhawejwewfeqq':
            dc[k]=dc[k]+1
        print dc


    #有序字典（普通字典的key是无序的，在对dict迭代的时候，无法确定key的顺序）
    def morderdict(self):
        od=OrderedDict()
        od['z']=1
        od['y']=2
        od['x']=3
        print od.keys()  #如何做一个FIFO

    def mCounter(self):
        mc=Counter()
        for ch in 'prgonagere':
            mc[ch]=mc[ch]+1
        print mc.keys()
        print mc.items() #返回字典

if __name__== "__main__":
    mcoll=collectionCT()
    #mcoll.mdeque();
    mcoll.mdefaultdict()
    #mcoll.mCounter()