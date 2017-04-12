## Flask学习笔记

[TOC]

### 基础

#### 项目目录结构

```
一个项目往往有很多文件，为了更好的对项目进行管理，同时也为了后期的扩展，需要好好设计一下工程的骨架结构。
删除之前的app.py文件，创建如下的目录结构
├── app --app包目录
│ ├── __init__.py --初始化app包
│ ├── models.py --数据模型
│ ├── static --静态文件目录
│ │ ├── bootstrap.css --样式文件
│ │ └── index.css --样式文件
│ ├── templates --模板目录
│ │ └── index.html --模板文件
│ └── views.py --视图
├── config.py --应用配置信息，比如数据库配置
├── manage.py --脚本，比如启动服务器，与数据库交互
├── README.md --项目的说明
├── requirenments.txt --项目依赖
└── run.py --项目运行脚本
```



## 参考

[Flask快速入门](http://www.pythondoc.com/flask/quickstart.html#web)(推荐)

[Flask数据库操作](http://flask-sqlalchemy.pocoo.org/2.1/)

[Flask和Nginx的对接](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04)

[知乎的Flask专栏](https://zhuanlan.zhihu.com/flask)