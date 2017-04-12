#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：md5和sha1
  Ref:https://funhacks.net/explore-python/Standard-Modules/hashlib.html
'''
import  hashlib

'''
    基础：算法测试
'''
# 文件的md5校验
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


# 文件的sha1校验（常用语数字签名）
def mSHA1():
    sha1=hashlib.sha1()
    sha1.update('sha1 test')
    sha1.update('in Python')
    print sha1.hexdigest()

'''
    应用：大文件的md5校验
    Ref:http://blog.csdn.net/linda1000/article/details/17581035
'''
def bigf_md5():
    pass



# 测试入口
if __name__ == "__main__":
    mMD5()
