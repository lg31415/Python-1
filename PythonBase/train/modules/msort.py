#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''
'''
要求：
    1,所有的小写字母在大写字母前面
    2,所有的字母在数字前面
    3,所有的奇数在偶数前面
'''
def run():
    s = "Sorting1234!"
    res="".join(sorted(s, key=lambda x: (x.isdigit(), x.isdigit() and int(x) % 2 == 0, x.isupper(), x.islower(), x)))
    print res

if __name__ == "__main__":
    run()
