#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：retry模块学习
  参考链接：http://segmentfault.com/a/1190000004085023
            http://www.jb51.net/article/46641.htm
'''

import random
from retrying import  retry


@retry(stop_max_attempt_number=5,stop_max_delay=10)
def mretry():
    if random.randint(0,10)!=5:
        print "It's not 5!"
        raise  Exception("it is not 5!")
    print "It's 5！"


if __name__ == "__main__":
    mretry()
