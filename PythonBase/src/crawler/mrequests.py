#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：requests库的使用
  参考：https://funhacks.net/explore-python/HTTP/Requests.html
  状态：未完成
'''

import json
import requests


def mrequests():
    url='http://longtail.v.xunlei.com/readnotice?userid=123456&sessionid=xxx&bussinessid=-1'
    url="http://longtail.v.xunlei.com/setuser?userid=123456&sessionid=xxx&bussinessid=-1"
    url="http://testlua.com/lua_file"

    #postbody = {'id': 1, 't': 123232320}
    postbody={
        "info":{
            "nickname":"user",
            "sign":"hahahahahaha",
            "sex":0,
            "phone_num":"13800000000",
            "email":"xxx@qq.com",
            "birth_day":"1988-11-11",
            "image":"http://image.jpg"
        },
        "t":1482302070
    }

    r = requests.post(url, data=postbody)            # 发数编码为表单形式的数据
    #r = requests.post(url,data=json.dumps(postbody))# 发送编码为string形式的数据
    #r = requests.post(url,json=postbody)            # 等同于上个

    print r.text


# 测试入口
if __name__ == "__main__":
    mrequests()
