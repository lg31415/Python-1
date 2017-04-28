#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：python字符串处理
'''
import os

# 字符串基本处理
def mstrbasic():
    #判断字符串是否为空
    ms='  '
    if ms.strip()=='':
        print("ms is null")
    if not ms.strip():
        print 'ms is  null2'

    # 去掉字符串两边指定字符
    ms='2345sdwe34'
    st=ms.strip('234') #
    print(st)

#字符串查找
'''
    Python字符串查找的四个方法：find(),index(),rfind(),rindex()
    source:http://outofmemory.cn/code-snippet/6682/python-string-find-or-index
'''
def mstrfind():
    mstr='bnawer4 wewr4w'
    print mstr.rfind('r',2,7) #若查找成功，返回从0开始的下标值，否则返回-1
    print(len(mstr))
    print mstr.rindex('w')   #查找字符串第一次出现的位置，若查找不到，抛出异常

#字符串拼接及字典，元组和字符串之间的转换
def mstrmerge():
    mstr='12345678'
    mstrlist=list(mstr)
    print(mstrlist)
    strmerge=''.join(mstrlist)
    print strmerge
    mstrtuple=tuple(mstr)
    print mstrtuple
    mstrtuplemerge=''.join(mstrtuple)
    print(mstrtuplemerge)

    list2tuple=tuple(mstrlist)
    print(list2tuple)

#字符串切分
def mstrsplit():
    sinline = 'name:haha,age:20|name:python,age:30|name:fef,age:55'
    print sinline.split('|')
    #更详细的用法
    u = "www.doiido.com.cn"

    #使用默认分隔符
    print u.split()
    #以"."为分隔符
    print u.split('.')
    #分割0次
    print u.split('.',0)
    #分割一次
    print u.split('.',1)
    #分割两次
    print u.split('.',2)
    #分割两次，并取序列为1的项
    print u.split('.',2)[1]
    #分割最多次（实际与不加num参数相同）
    print u.split('.',-1)
    strsplit='using  the default'.split() #会去除两边的空格
    print(strsplit)

    mutiline= """Hello!!!
    Wellcome to Python's world!
    There are a lot of interesting things!
    Enjoy yourself. Thank you!"""
    muti2sinline=''.join(mutiline.splitlines())
    print(muti2sinline)

    #os.path.split函数
    print os.path.split('\jhwe\we\ss.txt')[1] #得到分割的元组
    print os.path.splitext('\jhwe\we\ss.txt')[1]  #直接获取文件扩展名
    print os.path.splitdrive('C:\jhwe\we\ss.txt')[0]  #直接获取盘符


#字符串格式化
def mstrformat():
    print("{} {}".format("Hello", "World"))
    # is equal to...
    print("{0} {1}".format("Hello", "World"))
    print("{hello} {world}".format(hello="Hello", world="World"))
    print("{0}{1}{0}".format("H", "e"))

    #解包
    c="{hello} {world}".format(**{"hello":"yjm", "world":"python"})
    print "+++c:",c
    print("{} {}".format(*["Python", "Rocks"]))
    #等同于
    data = {'name': 'Python', 'score': 100}
    print("Name: {0[name]}, Score: {0[score]}".format(data)) # 不需要引号
    langs = ["Python", "Ruby"]
    print("{0[0]} vs {0[1]}".format(langs))

    #对齐和填充
    #for align,text in zip





if __name__ == "__main__":
    #mstrnull()
    #mstrip()
    #mstrfind()
    #mstrmerge()
    #mstrsplit()
    mstrformat()
