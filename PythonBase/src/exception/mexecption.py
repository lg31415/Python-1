#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python异常捕获和处理解决
'''

import sys

def raiseException(n):
    try:
        if n==0:
            raise ValueError("invalid n")
        else:
            print("all is ok")
    except ValueError,e:
        print("Value Errror: %s") %str(e)
        s=sys.exc_info()
        print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)

    return 0


'''
  try...except...else..finally
  else 则用于处理没有出现错误的情况；finally 负责 try 语句的”善后工作“ ，无论如何都会执行
'''
def divide(x, y):
    try:
        result = x / y
    except ZeroDivisionError,e:
        print("division by 0!")
        s=sys.exc_info()
        print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)
    else:
        print("result = {}".format(result))
    finally:
        print("divide finished!")


# 程序主体
if __name__ == "__main__":
    #raiseException(0)
    divide(5,2)
    print("*"*20)
    divide(5,0)
