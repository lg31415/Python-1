#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：列表生成器
'''


def myield():
    g = (x * x for x in range(10))
    print g.next(),g.next()
    for item in g:
        print(item)

'''
每次调用next()的时候，遇到yield语句就返回，再次执行时从上次返回的yield语句出继续执行。
'''
def fib(max):
    n, a, b = 0, 0, 1
    print('--1-')
    while n < max:
        print('-2--',n)
        yield b
        a, b = b, a + b
        n = n + 1



if __name__ == "__main__":
    #myield()
    #print type(fib(2))
    for i in fib(3):
        print(i)
    o=fib(12)
    o.next()
    o.next()


