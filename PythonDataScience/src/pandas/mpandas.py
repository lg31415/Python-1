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


# Series（一维不同质可变长数组）
def mSeries():
    a=pd.Series(range(5))
    s=pd.Series([1,3,4,np.nan,6,8],index=['a','b','c','d','e','g'])  # 列表法
    s=pd.Series({'a':[1,2,3,4],'b':[6,7,8],'c':{284, 34}})           # 字典法
    s = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'],index=list("nibushigh"))
    mask=s.isin(['a','d'])
    print s.value_counts()
    print s[mask]

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

#DataFrame(基础)
def mDataFrame():
    dates=pd.date_range('20140202',periods=6)
    df=pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
    #df.to_excel('hhah.xlsx',sheet_name='nigao')
    #print df
    #df=df.cumsum()
    #plt.figure()
    #df.plot()
    #plt.legend(loc='best')
    #plt.show()

    df1=pd.DataFrame({'id':[1,2,3,4,5],"raw_grade":['a','b','c','d','e']})
    df1['grade']=df1.raw_grade.astype('category')
    df1.grade.cat.categories=['very good','good','very bad']
    df1.grade=df1.grade.cat.set_categories



#数据帧
def mDataframe_build():
    # Dataframe构建方式1：key是列，行元素分别是每个value，一一对应
    data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
             'year': [2000, 2001, 2002, 2001, 2002],
             'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
    frame1 =pd.DataFrame(data,columns=['pop','year','state','noc'],index=list('ABCDE'))
    print frame1,frame1.state,frame1['state'],frame1.ix['A']
    print '--------------------------------------------------------'

    # Dataframe构建方式2(逐行构建，列名由自己指定)
    datal=[['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],[2000, 2001, 2002, 2001, 2002], [1.5, 1.7, 3.6, 2.4, 2.9]]
    frame2=pd.DataFrame(datal,columns=['state','year','pop','add1','add2'])
    print frame2
    print '--------------------------------------------------------'

    # Dataframe构建方式3（嵌套字典）
    data3 = {'Nevada': {2001: 2.4, 2005: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
    frame3=pd.DataFrame(data3)
    print frame3,frame3.T
    print '--------------------------------------------------------'

    #Dataframe构建方式4（由numpy矩阵构建）
    data4=np.arange(6).reshape(2,3)
    print data4
    frame4=pd.DataFrame(data4,columns=['col1','col2','col3'],index=['row1','row2'])
    print frame4
    print '--------------------------------------------------------'

    #Dataframe构建方式5（由pd.Series构建）
    data5={"col1":pd.Series(np.arange(5),index=['r1','r2','r3','r4','r5']),"col2":pd.Series(['y','x','t','v','c'],index=['r1','r2','r3','r4','r5'])}
    print data5
    frame5=pd.DataFrame(data5,columns=['col1','col2','col3'],index=['r1','r2','r3','r4','r5'])
    print frame5
    print '--------------------------------------------------------'



# 索引和切片
def mDataFrame_select():
    data=pd.DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
    print data


# 数据帧统计处理
from datetime import  datetime,timedelta,date
def dataStat():
    pdata=pd.read_table('../../data/install',header=None,names=['datec','newi','totali'])
    #将整型转换成日期
    year=map(lambda x:int(str(x)[0:4]),pdata['datec'])
    month=map(lambda x:int(str(x)[4:6]),pdata['datec'])
    day=map(lambda x:int(str(x)[6:8]),pdata['datec'])
    pdata['datec']=map(lambda x:date(x[0],x[1],x[2]),zip(year,month,day))

    #统计最大值，最小值，和均值等
    maxnewi,minnewi,sumnewi=max(pdata['newi']),min(pdata['newi']),sum(pdata['newi'])
    maxtotali,mintotali,sumtotali=max(pdata['totali']),min(pdata['totali']),sum(pdata['totali'])

    maxv=pdata.max()
    minv=pdata.min()
    sumv=pdata.sum()
    maxnewi,maxtotali=maxv['newi'],maxv['totali']
    minnewi,mintotali=minv['newi'],maxv['totali']

    #分组统计(有问题)
    '''
    groupd=pdata.groupby(['datec'])
    pd.expanding_sum()
    print pdata
    print pdata.dtypes
    #print pdata.groupby('datec').sum()
    '''

    # pandas按指定条件进行分组汇总(这里主要是日期)：http://toutiao.com/i6321318705200366081/
    pdata = pdata.set_index('datec')
    groupd1=pdata.resample('M',how=sum).fillna(0)
    print groupd1





# 连接
def pJoin():
    #按默认的相同列名合并
    orders=pd.DataFrame(pd.read_csv('../../data/mjoin/orders.csv'))
    persons=pd.DataFrame(pd.read_csv('../../data/mjoin/persons.csv'))
    print orders
    print persons
    lj=pd.merge(orders,persons,how='left')
    print lj

    #按指定的列名合并
    pv=pd.DataFrame(pd.read_table('../../data/mjoin/date_fu2_pv',header=None,names=['date','fu2','pv']))
    uv=pd.DataFrame(pd.read_table('../../data/mjoin/date_fu2_uv',header=None,names=['date','fu2','uv']))
    lj=pd.merge(pv,uv,how='left',left_on=['date','fu2'],right_on=['date','fu2'])
    print  lj




# 利用字典实现pandas的构建
import MySQLdb
import numpy as np
def buildpandaFromSql():
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='study')
    cur=conn.cursor() #cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("select date,cnt,cnt_user from row2col_tbl limit 3")
    sqllist=cur.fetchall()
    sqlarray=np.array(sqllist,dtype='int')  #注意指定数据类型，否则会出错
    sqlframe=pd.DataFrame(sqlarray,columns=['date','cnt','cnt_user'],index=range(len(sqllist)))
    print sqlframe
    # numpy数组直接统计
    print sqlarray.any()



# 保存和读取sql
from sqlalchemy import create_engine
def readwritesql():
    engine = create_engine('mysql+mysqldb://root:root@localhost/study')

    # tomysql
    data=pd.read_csv('../../data/data.csv',header=False)
    print data,'\n',type(data)
    #data1=pd.DataFrame(['23.23',12,'ZHNWR','232'])
    data.to_sql('data',engine,if_exists='replace',index=False,chunksize=1000)

    #from mysql
    pr=pd.read_sql_table('data',engine,index_col=['fu5'],columns=['num'])
    print pr
    pq=pd.read_sql_query("select num from data order by num",engine)
    print pq



#保存和读取xls
def readwirtexls():
    #from csv
    data=pd.read_csv('../../data/data.csv',header=False,index_col='fu5')
    print data
    #to csv
    data.to_csv('../../data/data1.csv',columns=['num'],header=True,index=True,index_label=range(2,30))


if __name__ == "__main__":
    # mSeries()
    # mDataFrame()
    # mDataframe_build()
    # mDataFrame_select()
    dataStat()
    # pJoin()
    #buildpandaFromSql()
    # readwritesql()
    #readwirtexls()


