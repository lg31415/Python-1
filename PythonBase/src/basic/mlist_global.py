#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
    解释列表的使用和全局变量的使用
'''
##列表矩阵的访问
def listMatrix():
    M=[[1,2,3],
       [23,23,4],
       [23,2,1]]
    print 'row1:',M[0]          #打印第一行
    col2=[row[1] for row in M]  #打印第二列
    print 'col2:',col2

##全局变量的使用方法1
global glist
def globalM():
    #global list #声明使用的是全局变量
    glist=[]
    glist.append('123')
    glist.append('2344')
    print 'globalInner:',glist


##全局变量的使用方法2
CONSTANT = 0
  
def modifyGlobal():  
    global CONSTANT  #声明使用的是全局变量
    print(CONSTANT)  #原始的全局变量
    CONSTANT += 1
    print 'globalInner:',CONSTANT
  
 
if __name__ == '__main__':
    listMatrix()
    globalM()
    print 'globalExtern:',glist  #ERROR:global name 'glist' is not defined
    modifyGlobal()
    print 'globalExtern:',CONSTANT

