## web.py学习笔记

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



## 参考

[web.py官方新手指南](http://webpy.org/tutorial3.zh-cn)