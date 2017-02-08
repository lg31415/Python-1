#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：迭代工具
  参考：http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013994173393204e80af1f8fa94c8e9d094d229395ea43000
'''

import  itertools

def run():
    naturals=itertools.count(3)
    ns = itertools.takewhile(lambda x: x <= 10, naturals) #从无限序列中取序列
    for i in ns:
        print(i)

    '''
    cs=itertools.cycle('ABC')
    for i in cs:
        print(i)
    '''
    rs=itertools.repeat('ABC',4)
    for i in rs:
        print(i)

    for c in itertools.chain('ABC', 'XYZ'):
        print c

if __name__ == "__main__":
    run()
