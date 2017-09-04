#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:通过字典函数实现if-else的判别
    Ref:
    State：
    Date:2017/9/1
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

def default_fun():
    sys.exit()

def fun1():
    print "fun1"

def fun2():
    print "fun2"

def main():
    fundict={
        "1":fun1,
        "2":fun2
    }

    fid=raw_input("select fun id,press any other key to exit!\n>")
    print "fid:",str(fid)
    while fid!='':
        fundict.get(fid,default_fun)()
        fid=raw_input("select fun id,press any other key to exit!\n>")


# 测试入口
if __name__ == "__main__":
    main()

