#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''
import  hashlib

def mMD5():
    sdata="hellomd5"
    md5=hashlib.md5()
    md5.update(sdata)
    r1=md5.hexdigest()

    sdata_1="hello md5"  #验证出对空格敏感
    md5_1=hashlib.md5()
    md5_1.update(sdata_1)
    r2=md5_1.hexdigest()

    if(r1==r2):
        print("equal")
    else:
        print('noequal')


if __name__ == "__main__":
    mMD5()
