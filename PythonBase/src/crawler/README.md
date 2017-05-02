## Python爬虫梳理

[TOC]

### 概览

- bs4

解析html,xml文档的利器

- urllib,urllib2,urllib3

基本的web工具

- requests

功能强大，接近底层

- 其它

### 基础

#### bs4

Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象,所有对象可以归纳为4种:

- Tag
- NavigableString
- BeautifulSoup
- Comment

Tab

```
可以直接利用soup加标签名轻松地获取标签的内容，例如soup.p，查找的是所有内容中第一个符号要求的标签，如果要查询所有的标签，则利用后面的介绍。

soup.name和soup.attrs输出节点的标签名和属性字典
```

NavigableString

```
#获取标签内的内容,利用.string属性，返回的是NavigableString对象
soup.p.string
```

BeautifulSoup

```
# 文档的全部内容对象，可以当作是一个特殊的Tag
```

Comment

```
# 一个特殊的NavigableString对象，输出的内容不包括注释符号
```

判读当前节点的对象是什么

```python
import bs4 # 或者
from bs4 import Tag,NavigableString
if isinstance(par,bs4.element.Tag): #或者if isinstance(par,Tag)
	print 'now is Tag'
```



##### 查找

###### 遍历文档树

直接子节点

```
.contents属性，返回直接子节点的列表
.children属性，返回可迭代的子节点对象

for child in  soup.body.children:
    print child
```

所有子节点

```
.descendants对所有子孙节点进行递归循环，返回可迭代对象
for child in soup.descendants:
    print child
```

单个节点内容

```
.string属性
如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容。
```

所有节点内容

```python
# .strings和.stripped_strings返回文档所有节点的内容可迭代对象，后者去除了多余的空白内容
for cc in tag.stripped_string:
	print cc
    
# 类似的还有.text属性，该属性直接返回unicode格式的节点内容（带格式）
```

父节点

```python
# .parent属性,返回的是父节点的tag对象
```

全部父节点

```python
# .parents属性,返回的是全部父节点可迭代对象，从内层到外层逐层迭代，每层都是个tag对象
```

兄弟节点

```python
# 兄弟节点是和本节点处于同一级的节点
# next_sibling获取下一个，.previous_sibling 则与之相反，如果节点不存在，则返回 None,注意该返回值通常是\n等换行符，这是排版html格式的时候引起的
```

全部兄弟节点

```python
# .next_siblings  .previous_siblings 属性
```

前后节点

```python
# 不针对于兄弟节点，而是在所有节点
# .next_element  .previous_element 属性,其等同于.next和.previous
```

所有前后节点

```python
# .next_elements  .previous_elements 属性,逐层解析到最后
```

###### 依据DOM查找

list = ==find_all==() 

```
---- name标签
# 传tag标签的字符串
# 传包含tag标签的正则表达式
# 传列表
# 传方法
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
soup.find_all(has_class_but_no_id)

--- keyword参数
soup.find_all(href=re.compile("elsie"), id='link1'，'class_'='classname')
# [<a class="sister" href="http://example.com/elsie" id="link1">three</a>]

data_soup.find_all(attrs={"data-foo": "value"})
# [<div data-foo="value">foo!</div>]

---  text参数
搜索包含内容

----- recursive 参数
调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False .
```

find( name , attrs , recursive , text , **kwargs )

```
它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果
```

find_parents()  find_parent()

```
find_all() 和 find() 只搜索当前节点的所有子节点,孙子节点等. find_parents() 和 find_parent() 用来搜索当前节点的父辈节点,搜索方法与普通tag的搜索方法相同,搜索文档搜索文档包含的内容
```

find_next_siblings()  find_next_sibling()

```
这2个方法通过 .next_siblings 属性对当 tag 的所有后面解析的兄弟 tag 节点进行迭代, find_next_siblings() 方法返回所有符合条件的后面的兄弟节点,find_next_sibling() 只返回符合条件的后面的第一个tag节点
```

find_previous_siblings()  find_previous_sibling()

```
这2个方法通过 .previous_siblings 属性对当前 tag 的前面解析的兄弟 tag 节点进行迭代, find_previous_siblings() 方法返回所有符合条件的前面的兄弟节点, find_previous_sibling() 方法返回第一个符合条件的前面的兄弟节点
```

find_all_next()  find_next()

```
这2个方法通过 .next_elements 属性对当前 tag 的之后的 tag 和字符串进行迭代, find_all_next() 方法返回所有符合条件的节点, find_next() 方法返回第一个符合条件的节点
```

find_all_previous() 和 find_previous()

```
这2个方法通过 .previous_elements 属性对当前节点前面的 tag 和字符串进行迭代, find_all_previous() 方法返回所有符合条件的节点, find_previous()方法返回第一个符合条件的节点
```

> **注：以上（2）（3）（4）（5）（6）（7）方法参数用法与 find_all() 完全相同，原理均类似，在此不再赘述。**



###### 依据CSS查找

soup.select(),返回类型是list

##### 修改

###### 修改已有的

修改tag的名称和属性

```
tag['id']=xxx
tag['class']=xxx
tag['style']="position: absolute;  background-color:yellow;top: 0;right: 0;color:red"
del tag['id']
```

修改tag的内容

```
.string 方法
# 如果当前的tag包含了其它tag,那么给它的 .string 属性赋值会覆盖掉原有的所有内容包括子tag
```

向tag内添加新内容

```
.append()
```

###### 增加新的

> 方法汇总：
>
> - append
> - insert
> - insert_before()和insert_after()
> - clear() # 移除当前tag的内容
> - extract() #移除tag节点  

添加文本内容

```python
soup = BeautifulSoup("<b></b>")
tag = soup.b
tag.append("Hello")
new_string = soup.new_string(" there")
tag.append(new_string)
tag
# <b>Hello there.</b>
tag.contents
# [u'Hello', u' there']
```

添加新节点

```python
soup = BeautifulSoup("<b></b>")
original_tag = soup.b

new_tag = soup.new_tag("a", href="http://www.example.com")
original_tag.append(new_tag)
original_tag
# <b><a href="http://www.example.com"></a></b>

new_tag.string = "Link text."
original_tag
# <b><a href="http://www.example.com">Link text.</a></b>
```

#### urllib2

和urllib的关系

#### requests

怎样配合cookie等访问使用，

#### selenium

web自动化测试工具，的Webdriver操作浏览器。Selenium可以操作大多数主流浏览器（可能需要相应的驱动），当然也可以操作无界面的浏览器PhantomJS

##### PhantomJS

无界面浏览器，提供了js接口，windows平台的phantom.js接口可执行的exe，下载phantomJS并将其执行文件路径添加到PATH环境变量里

selenium操作PhantomJS

```python
from selenium import webdriver

driver = webdriver.PhantomJS()    # 获取浏览器对象
driver.get('http://www.baidu.com/')
print driver.page_source
```

##### chrome

selenium操作chrome浏览器，需要chromedriver.exe,将该可执行文件放到PATH环境变量里即可，注意和chrome的版本对应关系,如何退出程序后，清退所有的后台程序

selenium操作Chrome

```python
from selenium import webdriver

def sel_chrome():
	driver=webdriver.Chrome()
	driver.get('http://www.baidu.com')
	print driver.title
	print 'return'
```



参考：

[chromedriver.exe与chrome的对应关系和下载](http://blog.csdn.net/huilan_same/article/details/51896672)

### 优化

#### 多进程爬虫

-  [multiprocessing](https://docs.python.org/2/library/multiprocessing.html)

#### 多线程爬虫 

- thread,threading和Queue

## 参考

[Scrapy 爬虫 使用指南 完全教程](http://www.tuicool.com/articles/aMJvuu3)

[以生活例子介绍多线程和单线程](http://mp.weixin.qq.com/s?__biz=MjM5OTMxMzA4NQ==&mid=2655932144&idx=1&sn=2f6a122d5e0363f2dbb85fc2b7e406cd&scene=0#rd)

[Requests库的使用](https://funhacks.net/explore-python/HTTP/Requests.html)

[Python爬虫利器之BeautifulSoup的用法(静觅)](http://cuiqingcai.com/1319.html)

[BeautifulSoup官方文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#insert)

[书籍:Python 网络数据采集]()

 [Scrapy+PhantomJS+Selenium动态爬虫](http://blog.csdn.net/qq_30242609/article/details/70859891)

[Python爬虫爬取动态页面思路+实例（一）](http://blog.csdn.net/qq_30242609/article/details/53788228)

[深入理解Session与Cookie](https://my.oschina.net/kevinair/blog/192829)