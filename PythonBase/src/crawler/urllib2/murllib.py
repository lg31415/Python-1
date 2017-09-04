#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:urllib库的使用
    Ref:
    State：
    Date:2017/8/29
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib

class CUrllib():
    def __init__(self):
        pass
    def base(self):
        # 登陆用户名和密码
        data={
            "username":"张大哥",
            "password":"pass"
        }
        # urllib进行编码
        post_data=urllib.urlencode(data)
        print post_data




# 测试入口
if __name__ == "__main__":
    cl=CUrllib()
    cl.base()

