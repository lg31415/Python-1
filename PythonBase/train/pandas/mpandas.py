#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：pandas的数据结构Series和dataFrame
'''

import  pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

def unitily():
    version=pd.show_versions()
    print(version)


#序列化操作（一维不同质可变长数组）
def mSeries():
    a=pd.Series(range(5))
    s=pd.Series([1,3,4,np.nan,6,8],index=['a','b','c','d','e','g'])
    obj = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'],index=list("nibushigh"))
    print obj.value_counts()
    mask=obj.isin(['a','d'])
    print obj[mask]

    # 数据对齐
    d = {'a' : 0., 'b' : 1., 'c' : 2.}
    b=pd.Series(d)
    c=pd.Series(5., index=['a', 'b', 'c', 'd', 'e'])
    print a,b,c

    import matplotlib.pyplot as plt
    plt.hist(a,bins=3)
    plt.show()

    import seaborn
    seaborn.distplot(a,bins=3)

#数据帧
def mDataframe_build():
    # Dataframe构建方式1：key是列，行元素分别是每个value，一一对应
    data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
             'year': [2000, 2001, 2002, 2001, 2002],
             'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
    frame1 =pd.DataFrame(data,columns=['pop','year','state','noc'],index=list('ABCDE'))
    print frame1,frame1.state,frame1['state'],frame1.ix['A']

    # Dataframe构建方式2
    datal=[['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],[2000, 2001, 2002, 2001, 2002], [1.5, 1.7, 3.6, 2.4, 2.9]]
    frame2=pd.DataFrame(datal,columns=['state','year','pop','add1','add2'])
    print frame2

    # Dataframe构建方式3
    data3 = {'Nevada': {2001: 2.4, 2005: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    frame3=pd.DataFrame(data3)
    print frame3,frame3.T

    #Dataframe构建方式4
    data4=np.arange(6).reshape(2,3)
    print data4
    frame4=pd.DataFrame(data4,columns=['col1','col2','col3'],index=['row1','row2'])
    print frame4

    #Dataframe构建方式4
    data5={"col1":pd.Series(np.arange(5),index=['r1','r2','r3','r4','r5']),"col2":pd.Series(['y','x','t','v','c'],index=['r1','r2','r3','r4','r5'])}
    print data5
    frame5=pd.DataFrame(data5,columns=['col1','col2','col3'],index=['r1','r2','r3','r4','r5'])
    print frame5

# 索引和切片
def mDataFrame_select():
    data=pd.DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
    print data



if __name__ == "__main__":
    # mSeries()
    # mDataframe_build()
    mDataFrame_select()



