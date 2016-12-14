#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：高潮模式热力图历史数据的记录和分析
'''
import os,time
import re


'''
   PART1:历史数据备份
'''

# 当检测到文件改动的时候(并发)
'''
    这部分的功能交给调用者，在改动快照之前，先调用该脚本执行数据备份
    还是数据这边去检查（间隔检查5分钟），即找到最近5分钟修改过的文件，然后备份其内容
'''
def check_mod(path):
    filelist=[]
    # 获取当前时间
    curtime=time.time()
    for root, dirs, files in os.walk(path):
        for file in files:
            path= os.path.join(root, file)
            if (not re.match(r".*(\.svn).*", path)):
                dt=int(curtime-os.path.getmtime(file))
                if dt>300:
                    filelist.append(path)
    return  filelist


# 对并发情况的处理
'''
    并发情况由调用者处理，此处只提供功能实现
'''
def history_record(filein):
    fout=open("resultout.txt","a+")
    # 获取文件的修改时间
    statinfo=os.stat(filein)
    fout.write(time.strftime("%Y%m%d%M",time.localtime(statinfo.st_mtime)))
    fout.write("\t")

    # 获取文件的数据
    fin=open(filein,"r")
    for line in fin:
        data=line.strip().split()
        # data=[1,2,3,4,5]
        fout.write('\t'.join(map(str,data)))
        fout.write('\n')

    fin.close()
    fout.close()

# 处理程序主体
def history_bak(filelist):
    for file in filelist:
        try:
            history_record(file)
        except Exception,e:
            print str(e)


'''
    PART2:数据分析：对记录到的数据进行方差，拖动次数，播放时长的统计
'''
import pandas as pd
import matplotlib.pyplot as plt

def record_analys(filein):
    df=pd.read_csv(filein,sep='\t',names=['date','foo', 'bar', 'baz','twe','wew'],dtype={'date':object} ,header=None)
    print df.dtypes # 数据类型判定
    # print df['foo']

    #统计
    print df.describe() #得到拖动次数和播放时长的平均值
    print df.cov()  # 计算协方差矩阵

    # 绘图(及保存)
    dp=df.cumsum()
    # plt.figure()
    dp.plot(x='date',y=['foo','bar','baz'],kind='kde',stacked=True)#,marker='D',color='r')
    plt.title("change pkot".decode('utf8'))
    #plt.xlabel("data".decode('utf8'))
    #plt.ylabel("quantity".decode('utf8'))
    plt.legend(loc='best')
    plt.show() # 显示和保存2选1
    #plt.savefig('../data/testdata.jpg')

    #数据保存
    #df.to_csv('../data/jaj.csv') #df.to_excel
    #pd.read_csv('../data/jaj.csv')


if __name__ == "__main__":
    #history_record()
    record_analys('../data/hotview.txt')
