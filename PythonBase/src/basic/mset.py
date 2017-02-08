#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：集合操作
'''


#集合的操作
def mset():
    setA={'a','cd',1,'wehjer'}
    setB={'a',2,'ef','cd'}
    setAB=setA | setB
    print('setAB:',setAB)
    setAD=setA.add('D') #错误，集合setAD仍然是空值，只是在集合A中添加了元素'D'
    print('setAD:',setAD)
    print setA
    setA.remove('D')
    print setA

    setTuidao={x*3 for x in 'abcdef'} #集合解析（集合推导式）
    print(type(setTuidao),setTuidao)


if __name__ == "__main__":
    mset()
