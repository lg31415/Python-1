#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python实现groupby功能
    Ref:
    State：
    Date:2017/6/28
    Author:tuling56
'''
import re, os, sys
import hues
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')

class PStat():
    def __init__(self):
        self.src_data='./groupby_data'
        self.posnum={}

    # 分组统计累和
    def groupby_sum(self):
         with open(self.src_data,'r') as f:
            for line in f:
                try:
                    pos,pv,uv=line.strip('\n').split()  #按第一列分组，对第二，三列就行汇总
                except Exception,e:
                    print str(e),line
                    continue

                if self.posnum.has_key(pos):
                    self.posnum[pos][1]+=int(pv)
                    self.posnum[pos][2]+=int(uv)
                else:
                    if pos=='movie':
                        self.posnum[pos]=[1,int(pv),int(uv)]
                    elif pos=='teleplay':
                        self.posnum[pos]=[2,int(pv),int(uv)]
                    elif pos=='tv':
                        self.posnum[pos]=[3,int(pv),int(uv)]
                    elif pos=='anime':
                        self.posnum[pos]=[4,int(pv),int(uv)]
                    elif pos=='vmovie':
                        self.posnum[pos]=[5,int(pv),int(uv)]
                    elif pos=='joke':
                        self.posnum[pos]=[6,int(pv),int(uv)]
                    elif pos=='mvzhibo': #(jiuwo)
                        self.posnum[pos]=[7,int(pv),int(uv)]
                    elif pos=='zhibo':
                        self.posnum[pos]=[8,int(pv),int(uv)]
                    elif pos=='documentary':
                        self.posnum[pos]=[9,int(pv),int(uv)]
                    elif pos=='femalestars':
                        self.posnum[pos]=[10,int(pv),int(uv)]
                    else: #unknown
                        self.posnum[pos]=[-1,int(pv),int(uv)]
         print self.posnum

    def __judge_range(self,value):
        value=int(value)
        if value>=0 and value<1024:
            return '[0,1)'
        elif value>=1024 and value<2048:
            return '[1,2)'
        elif value>2048 and value<3072:
            return '[2,3)'
        elif value>=3072 and value<4096:
            return '[3,4)'
        elif value>=4096:
            return '[4,)'
        else:
            return 'error'


    # 分组统计类合
    def groupby_count(self):
        res=defaultdict(0)
        with open(self.src_data,'r') as f:
            num=0
            for line in f:
                num=num+1
                ratio=str(round(num*100/7215226.0,2))+"%"
                hues.info("Process:"+ratio)
                try:
                    dt,fu2,fu6,fu7=line.split('\t')
                    dur=self.__judge_range(fu6)
                    flag='yes' if 'geforce' in fu7.lower() else "no"
                    key=dur+"\t"+flag
                    res[key]=res[key]+1
                except Exception,e:
                    print str(e)
        f=open("ww_mem_geforce_dist","w")
        for k,v in res.iteritems():
            f.write(k+"\t"+str(v)+'\n')
        f.close()

# 测试入口
if __name__ == "__main__":
    pstat=PStat()
    pstat.groupby_count()

