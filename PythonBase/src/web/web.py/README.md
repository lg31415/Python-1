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

```python
import web
 
urls = ('/hello', 'hello',
       )
 
class hello(object):
  def GET(self):
    return 'hello world'
 
if __name__ == "__main__":
  app = web.application(urls, globals())  #其中的globals()参数必不可少
  app.run()
```

> 在命令行运行的指定iP和端口`python demo.py 127.0.0.1:8080`

### 模块

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