# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：目录遍历
  参考1：Python文件和路径的操作函数，http://www.jb51.net/article/21007.htm
  参考2：os.path下的的函数：http://blog.sina.com.cn/s/blog_a322be3f01016lkb.html
  注意区分
'''

import os
import sys

'''
    列出当前目录的文件和文件夹
'''
def mdir():
    os.chdir('E:\Python')
    path=os.getcwd()
    print path
    for file in os.listdir(path):
        if(os.path.isdir(file)):
            print 'Dir',file
        else:
            print 'File',file
        #选出指定格式的文件
        if file.endswith('.txt'):
            print "txt文件"

#切换到当前目录的上一级目录
'''
 参考链接：http://www.douban.com/group/topic/60828577/?cid=745942016
 os.path.dirname(path) 函数获取路径的上一级目录
'''
def chpardir():
    #方法一
    curdir=os.getcwd()
    pardir=os.path.dirname(curdir)
    print(curdir,pardir)

    #方法二
    path1=os.path.dirname('mdir.py') #如果该文件
    print 'path1:',path1
    path2=os.path.join(path1,os.path.pardir)
    print 'path2:',path2
    path3= os.path.abspath(path2)
    print 'path3:',path3

def ospathdir():
    os.uname() #获取操作系统信息(在windows上不提供)
    print [x for x in os.listdir('.') if os.path.isdir(x)] #列出所有目录
    print [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'] #列出某种类型的文件

'''
    切换到当前目录的上n级目录
'''
def chrndir(curdir,n):
    print(curdir)
    if not os.path.exists(curdir):
        print "[not exits]:",curdir
        return  1
    if n>curdir.count(os.sep):
        print "no enough dir"
        return 2;
    return  curdir.rsplit(os.sep,n)[0]
    # ndir=os.sep.join()



if __name__ == "__main__":
    #mdir()
    #chpardir()
    print chrndir(os.getcwd(),2)