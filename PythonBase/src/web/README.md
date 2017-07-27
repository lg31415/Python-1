## Python Web开发综述

[TOC]

### 基础知识

#### 超时

超时问题，在网络环境不好的情况下，时常出现read()方法没有任何反应的超时问题，程序卡死在read()方法里，设置了超时之后，read超时的时候就会抛出socket.timeout异常，还需要给urlopen加上异常处理，再加上出现异常重试，

```python
import urllib2 

# 方法2（设置全局超时）
import socket
socket.setdefaulttimeout(10.0) 
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded'}

url='http://www.facebook.com/' 
fails = 0 
while True: 
    try: 
        if fails >= 20: 
            break
        req = urllib2.Request(url,req_header) 
        response = urllib2.urlopen(req, None, timeout=3)  # 方法1（设置timeout参数）
        page = response.read() 
   	except Exception,e: 
        fails += 1 
        print '网络连接出现问题, 正在尝试再次请求: ', fails 
    else: 
         break
            
            
# 方法3：（使用定时器）
from threading import Timer
url = "http://www.python.org"
def handler(fh):
    fh.close()
fh =urllib2.urlopen(url)
t = Timer(20.0, handler,[fh])
t.start()
data = fh.read()    #如果二进制文件需要换成二进制的读取方式
t.cancel()
```

参考：

[urllib2超时问题](http://blog.csdn.net/waterforest_pang/article/details/16885259)

[python使用urllib2设置超时时间](http://blog.chinaunix.net/uid-12014716-id-5763287.html)

### 开发框架

| 框架       | 简介   | 优点   | 缺点   |
| -------- | ---- | ---- | ---- |
| flask    |      |      |      |
| tornordo |      |      |      |
| django   |      |      |      |
| web.py   |      |      |      |
| bottle   |      |      |      |

#### flask

轻量级，但功能强大，开发方便

进度：

> 2017年4月17日

开始准备学习

#### django

功能全面

#### web.py

轻量级，正在使用

进度

##### 基础

表单数据获取

```
web.input(),获取url参数，返回值是类似于字典的key-value对,可以用于GET和POST。
web.data(),获取实体正文，返回值是一个字符串，只能用于POST。
```

##### 参考

[web.py中url总结](https://my.oschina.net/yangyanxing/blog/170418)

#### bottle





## 参考

