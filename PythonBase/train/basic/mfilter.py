# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：filter函数
'''

#过滤函数必须返回布尔值
def ffilter(x):
    return x.isalpha()

def mfilter():
    l=list('he234llo')
    l_filter=filter(ffilter,l)
    print(l_filter)


if __name__ == "__main__":
    mfilter()
