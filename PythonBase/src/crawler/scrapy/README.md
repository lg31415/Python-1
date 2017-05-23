##Scrapy学习笔记
[TOC]

### 基础

#### 安装

```
pip  install scrapy
```

#### 创建和运行爬虫项目

创建

```shell
scrapy startproject scrapydemo
```

> 目录结构如下：
>
> ```
> scrapydemo/	 # 项目配置文件
> ├── scrapy.cfg	
> └── scrapydemo
>     ├── __init__.py
>     ├── items.py	    # 用来存储爬下来的数据结构（字典形式）
>     ├── middlewares.py  
>     ├── pipelines.py	# 用来对爬出来的item进行后续处理，如存入数据库等
>     ├── settings.py		# 爬虫配置文件
>     └── spiders			# 此目录用来存放创建的新爬虫文件（爬虫主体）
>         └── __init__.py
> ```

执行

```shell
# 方法1
cd scrapydemo
scrapy genspider example example.com

# 方法2
cd scrapydemo/spiders
scrapy crawl scrapyname
```

> 注意：
>
> 此处的scrapyname是爬虫的名字，是spiders目录下的的爬虫脚本，爬虫名字的指定方式如下:
>
> ```python
> # -*- coding: utf-8 -*-
> import scrapy
> from myfirstscrapy.items import MyfirstscrapyItem
> import logging
>
> class MyfirstscrapySpider(scrapy.Spider):
>     name = "myfscrapy"
>     allowed_domains = ["njupt.edu.cn"]
>     start_urls = [
>         "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/1/list.htm",
>         ]
> ```

#### 爬虫框架流程

1. 创建工程

scrapy startproject njupt #其中njupt是项目名称，可以按照个人喜好来定义

2. 设置item

定义要存储的内容

3. 编写spider

spider是爬虫的主体，负责处理requset response 以及url等内容，处理完之后交给pipelines进行进一步处理。

4. 编写pipelines

pipelines主要用于数据的进一步处理，比如类型转换、存储入数据库、写到本地等。其实pipelines是在每次spider中yield item之后调用，用于处理每一个单独的item

5. settings.py

settings.py文件用于存储爬虫的配置，此处简单的添加一个刚才编写的pipelines

6. 启动爬虫和查看结果

scrapy crawl njupt



 ##参考

[Scrapy爬取南邮新闻demo](http://python.jobbole.com/85281/)