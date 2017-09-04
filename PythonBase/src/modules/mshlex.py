#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:shlex模块用以分割引号内的文本和引号外的文本
    Ref:http://yaotiaochimei.blog.51cto.com/4911337/1157633/
    State：
    Date:2017/4/12
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import shlex
test_str='''
            This string has embedded "double quotes" and 'single quotes' in it,and even "a 'nested example'".
         '''
def mshlex():
    print shlex.split(test_str)
    tokens=shlex.shlex(test_str)
    for token in tokens:
        print repr(token)

# 测试入口
if __name__ == "__main__":
    mshlex()

