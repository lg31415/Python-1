## web.py学习笔记

[TOC]

### 前言

测试:

> /home/yjm/Projects/webframe/web.py/webpy_uwsgi

```
# 得到json数据：
http://testuwsgi.com/

# 使用表单数据
http://testuwsgi.com/form?name=二狗&age=100

# 使用表单数据和静态数据，jinja2模板渲染
http://testuwsgi.com/jinja2?date=zhang&name=ilovey
```

### 基础

搭建最基础的webpy应用程序

```python
import web
#web.config.debug = False

urls = (
    		'/hello', 'AbsoluteUrl',
    		'/hello/.*','AmbiguousUrl',
    		'/hello/(.*)','GroupUrl'
       )

# 完全匹配
class AbsoluteUrl:
    def GET(self):
        web.header('Content-type','text/html;charset=utf-8')
        return u'URL完全匹配'

# 模糊匹配
class AmbiguousUrl:
    def GET(self):
        web.header('Content-type','text/html;charset=utf-8')
        return u'URL模糊匹配'

#分组的url处理类
class GroupUrl:
    def GET(self,name):  #如果你这里是带组匹配，一定要添加参数,用来接收你返回的参数
        web.header('Content-type','text/html;charset=utf-8')
        return u'URL带组匹配--'+name

# 定义app    
app = web.application(urls, globals())  #其中的globals()参数必不可少
#app.config['debug'] = False
#　程序入口
if __name__ == "__main__":
	app.run()
else:
    application = app.wsgifunc()
```

> 在命令行运行的指定iP和端口`python demo.py 127.0.0.1:8080`，这种方式指定的只能本地访问，如需要外网访问，则需要使用python demo.py 80

#### 配置

> webpy结合uwsgi的配置说明，uwsgi --help, #一个启动配置文件的参考：

| [uwsgi]                                | 说明                                      |
| -------------------------------------- | --------------------------------------- |
| socket = 127.0.0.1:9000                | 通信                                      |
| master = true                          | 是否是主机                                   |
| processes = 1                          | 开启的进程数量                                 |
| daemonize = /usr/local/vod/log/vod.log |                                         |
| chdir = /usr/local/vod/                | 指定运行目录                                  |
| pidfile = /usr/local/vod/.pid          | 指定pid文件的位置，记录主进程的pid号                   |
| module = interface                     | 同级目录下有个interface.py的问文件，注意和wsgi-file的区别 |
| plugins = python                       | ***这个配置在python应用的时候必须开启***              |
| web.config.debug = False               | 是否开启debug模式                             |
| socket-timeout = 120                   | 超时设置                                    |
| harakiri = 1200                        |                                         |
| py-autoreload = 1                      |                                         |
| wsgi-file                              | 载入wsgi-file                             |
| stats                                  | 在指定的地址上，开启状态服务                          |
| thred                                  | 运行线程数量                                  |
| log-maxsize                            | 以固定的文件大小（kb），切割日志文件                     |
| vacuum                                 | 当服务器退出的时候自动清理环境，删除uinx socket和pid文件     |
| disable-logging                        | 不记录请求信息的日志，只记录错误及uwsgi内部消息到日志中。         |
| uid=root                               | 配置运行uwsgi用户的uid                         |
| gid=root                               | 配置运行uwsgi用户的gid                         |

#### URL控制

三种匹配模式：

```
URL完全匹配(具体的url) 
/index

URL模糊匹配(你根本就不知道index后面是什么，它根本不会返回参数) 
/index/\d

URL带组匹配(主要有个’()’,它的作用主要是返回参数，你处理的类中一定要有个参数接受) 
/baidu/(.*)
```



### 应用

#### 文件上传/下载

上传

```python
class Upload:
     def GET(self):
         web.header("Content-Type","text/html; charset=utf-8")
         return """<html><head><title>Upload</title></head><body>
		 <form method="POST" enctype="multipart/form-data" action="">
		 <input type="file" name="myfile" />
		 <br/>
		 <input type="submit" />
		 </form>
		 </body></html>"""
     def POST(self):
         x = web.input(myfile={})
         filedir = './' 
         if 'myfile' in x: # to check if the file-object is created
             filepath=x.myfile.filename.replace('\\','/') 
             filename="thisismy.file" 
             fout = open(filedir +'/'+ filename,'w') 
             fout.write(x.myfile.file.read()) # writes the uploaded file to the newly file.
             fout.close() # closes the file, upload complete.
         raise web.seeother('/upload')
```

下载

```python
class Download:  
    def GET(self):  
        file_name = 'file_name'  
        file_path = os.path.join('file_path', file_name)  
        f = None  
        try:  
            f = open(file_path, "rb")  
            webpy.header('Content-Type','application/octet-stream')  
            webpy.header('Content-disposition', 'attachment; filename=%s.dat' % file_name)  
            while True:  
                c = f.read(BUF_SIZE)  
                if c:  
                    yield c  
                else:  
                    break  
        except Exception, e:  
            print e  
            yield 'Error'  
        finally:  
            if f:  
                f.close()  
```

关于响应头设置

```python
# webpy下载文件需要指定Content-type和Content-Disposition头，如下代码：

web.header("Content-Type","text/csv;charset=utf-8") # content-type需要根据实际的文件类型来指定
web.header("Content-Disposition","attachment;filename=xxxx.jpg")
```

参考:

[web.py文件表单上传示例](http://www.cnblogs.com/catmelo/p/3898357.html)

[web.py大文件上传](http://outofmemory.cn/code-snippet/3335/webpy-upload-huge-file)

[web.py大块文件下载示例](http://fighter1945.iteye.com/blog/1409806)

## 参考

[web.py官方新手指南](http://webpy.org/tutorial3.zh-cn)