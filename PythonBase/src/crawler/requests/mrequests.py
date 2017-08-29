#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：requests库的使用
  参考：https://funhacks.net/explore-python/HTTP/Requests.html
  状态：未完成
'''

import json
import sys
import requests


'''
    requests库的使用
'''
class MCRequest():
    def __init__(self):
        pass

    # post请
    def req_post(self):
        url='http://longtail.v.xunlei.com/readnotice?userid=123456&sessionid=xxx&bussinessid=-1'
        url="http://testlua.com/lua_file"
        url="http://testuwsgi.com"

        #postbody = {'id': 1, 't': 123232320}
        postbody={
            "info":{
                "name":"user",
                "sign":"hahahahahaha",
                "age":0,
                "phone_num":"13800000000",
                "email":"xxx@qq.com",
                "birth_day":"1988-11-11",
                "image":"http://image.jpg"
            },
            "t":1482302070
        }

        #r = requests.post(url, data=postbody)            # 发数编码为表单形式的数据（直接传递字典）
        #r = requests.post(url,data=json.dumps(postbody))# 发送编码为string形式的数据（json数据）
        r = requests.post(url,json=postbody)            # 等同于上个（这种方式等价于使用 json 参数，而给它传递 dict）

        print r.text

    # get请求
    def req_get(self):
        #headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        mcookie={}
        geturlparas = {'page': '1', 'per_page': '10','Name':None}
        r = requests.get("http://httpbin.org/get", params=geturlparas)#,headers=headers，cookies=mcookie)

        # 查看请求
        print r.url
        print r.request.headers  # 查看发送的请求头

        # 查看返回
        print 'response_headers:',r.headers          # 服务器返回的响应头部信息
        cookie_dict=requests.utils.dict_from_cookiejar(r.cookies)
        print 'response_cookies:',cookie_dict          # 服务器返回的cookie信息

        print r.status_code
        print 'text:',r.text
        print 'json"',r.json()
        print '二进制"',r.content
        print '原始响应:',r.raw

    # 请求数据的时候发送cookie,需要服务器端来解析客户端发送的cookie数据并返回
    def req_get_cookie(self):
        mcookie=dict(key1='value1')
        #r=requests.get('http://testuwsgi.com/',cookies=mcookie)
        r=requests.get('http://httpbin.org/get',cookies=mcookie)  #传递的是字典数据
        print 'response_headers:',r.headers
        print 'response_cookies:',r.cookies


    # 会话处理
    def session(self):
        ms=requests.Session()
        # 可先get添加cookie,然后在会话中post的时候使用这个cookie
        cookies={}
        ms.get('',cookies=cookies)
        ms.post('')

        # 也可先post的方式登录指定的网站，然后get的时候使用登录后的cookie
        login_url=''
        login_data={'user':'abc','psw':123}
        ms.post(login_url,data=login_data)

        visit_url=''
        visit_data={"name":'二黑','age':10}
        ms.get(visit_url,visit_data)

        ms.close() #关闭会话



# 测试入口
if __name__ == "__main__":
    mreq=MCRequest()
    #mreq.req_post()
    #mreq.req_get()
    mreq.req_get_cookie()