#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:http头定义
    Ref:
    State：
    Date:2017/6/22
    Author:tuling56
'''


# 设置请求头
headers=[]
header_firfox={'User-Agent' : "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"}
header_chrome={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
header_edge={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"}
headers.append(header_firfox)
headers.append(header_chrome)
headers.append(header_edge)

# 设置代理
proxy_ips=[
    "http://10.10.1.10:3128"
]
