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

1. **创建工程**

scrapy startproject njupt #其中njupt是项目名称，可以按照个人喜好来定义

2. **设置item**

定义要存储的内容

3. **编写spider**

spider是爬虫的主体，负责处理requset response 以及url等内容，处理完之后交给pipelines进行进一步处理。

一个例子(利用BaseSpider实现)：

```python
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector	# 使用Xpath来解析数据
class DmozSpider(BaseSpider):
    name = "dmoz"		# 爬虫名字，不能重复
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",        		         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    
    # spider抓到一个网页以后默认调用的callback
    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
    
    # 解析网页内容
    def parse_2(self,response):
       hxs = HtmlXPathSelector(response)
       sites = hxs.select('//ul/li')
       items = []
       for site in sites:
           item = DmozItem()
           item['title'] = site.select('a/text()').extract()
           item['link'] = site.select('a/@href').extract()
           item['desc'] = site.select('text()').extract()
           items.append(item)
       return items       
```

当spider拿到url的内容后，会调用parse方法，并且传递一个response参数给parse函数，response包含了抓到的网页的内容，在parse方法里解析网页数据****

**连续spider**

实现1：

```python
class MySpider(BaseSpider):
    name = 'myspider'
    start_urls = (
        'http://example.com/page1',
        'http://example.com/page2',
        )
    def parse(self, response):
        # collect `item_urls`
        for item_url in item_urls:
            yield Request(url=item_url, callback=self.parse_item)
    def parse_item(self, response):
        item = MyItem()
        # populate `item` fields
        yield Request(url=item_details_url, meta={'item': item},
            callback=self.parse_details)
    def parse_details(self, response):
        item = response.meta['item']
        # populate more `item` fields
        return item
```

实现2：

```python
from scrapy.spider import CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MininovaSpider(CrawlSpider):
    name = 'mininova.org'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+'])),
             Rule(SgmlLinkExtractor(allow=['/abc/\d+']), 'parse_torrent')]
    def parse_torrent(self, response):
        x = HtmlXPathSelector(response)
        torrent = TorrentItem()
        torrent['url'] = response.url
        torrent['name'] = x.select("//h1/text()").extract()
        torrent['description'] = x.select("//div[@id='description']").extract()
        torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
        return torrent
```

4. **编写pipelines**

pipelines主要用于数据的进一步处理，比如类型转换、存储入数据库、写到本地等。其实pipelines是在每次spider中yield item之后调用，用于处理每一个单独的item

```python
from scrapy.exceptions import DropItem
class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""
    # put all words in lowercase
    words_to_filter = ['politics', 'religion']
    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item
```

可以在pipelines中对item进行过滤，pipeline处理的是所有使用`yield item`到pipeline的数据，所以在处理的时候要注意确保每个爬虫要爬取的字段内容是一致的

5. **settings.py**

settings.py文件用于存储爬虫的配置，此处简单的添加一个刚才编写的pipelines

6. **启动爬虫和查看结果**

```shell
# 基本
scrapy crawl njupt

# 添加-o和-t参数，将parse方法的items输出到json文件中 
scrapy crawl dmoz -o items.json -t json
```



 ##参考

[Scrapy爬取南邮新闻demo](http://python.jobbole.com/85281/)

[Python爬虫框架scrapy实例](http://www.pythontab.com/html/2013/pythonhexinbiancheng_0814/541.html)

[xpath获取节点和子节点的文本内容](http://www.tuicool.com/articles/iqQFBn)

[lxml的etree获取节点和子节点的内容](https://segmentfault.com/q/1010000004879947)