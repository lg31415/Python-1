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

节点内容

```
.string属性
如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容。
```

多个内容

```
.strings和.stripped_strings返回文档所有节点的内容，后者去除了多余的空白内容
```

父节点

```
.parent属性
```

全部父节点

```
.parents属性
```

兄弟节点

```
兄弟节点是和本节点处于同一级的节点
next_sibling获取下一个，.previous_sibling 则与之相反，如果节点不存在，则返回 None

```

全部兄弟节点

```
.next_siblings  .previous_siblings 属性
```

前后节点

```
# 不针对于兄弟节点，而是在所有节点，不分层次
.next_element  .previous_element 属性
```

所有前后节点

```
.next_elements  .previous_elements 属性
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



#### urllib2

#### requests

怎样配合cookie等访问使用

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

