#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：python容易出错的地方
'''

x=1
def run():
    global x  # 如果不加入个申明，则x=x+2提示错误
    x=x+2
    y=x+1
    print y


if __name__ == "__main__":
    run()
