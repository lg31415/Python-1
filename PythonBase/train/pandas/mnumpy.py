#-*-coding:utf-8-*-

###一些公用的模块文件
import os
import sys
import numpy
#from numpy import *

# 构建多维数组
def mnmpy():
    a = numpy.array([[[2,3,4,4],[4,5,6,6],[7,8,9,9]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ])
    print a, a.shape,type(a)


#不使用numpy(zip函数相当于对两个列表进行解包)
def mvectoradd(n):
    itemlist=range(n)
    a= [item**2 for item in itemlist]
    b=[item**3 for item in itemlist]
    ab=[]
    for aitem,bitem in zip(a,b):
        temp=aitem+bitem
        ab.append(temp)
    print a,'\n',b,'\n',ab

#使用numpy
def mvectoradd_numpy(n):
    a=numpy.arange(n)**2
    b=numpy.arange(n)**3
    c=a+b
    print(c)

if __name__ == "__main__":
    mnmpy()
    #mvectoradd(6)
    #mvectoradd_numpy(6)


