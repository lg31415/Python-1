## Python学习笔记

[TOC]

### 基础数据类型

#### 标准库模块

#### collections模块

- OrderedDict

> ```python
> >>> dict([('a', 10), ('b', 20), ('c', 15)])
> {'a': 10, 'c': 15, 'b': 20}
> ```
>
> 有时，我们希望保持 key 的顺序，这时可以用 OrderedDict：
>
> ```python
> >>> from collections import OrderedDict
> >>> OrderedDict([('a', 10), ('b', 20), ('c', 15)])
> OrderedDict([('a', 10), ('b', 20), ('c', 15)])
> #注意此处构造排序字典的时候不能使用如下的方式，该方式的key是无序的
> OrderedDict({'a'：10, 'b',：20, 'c'：15})
> ```

- defaultdict

> 使用默认字典，可以给字典中的key提供一个默认值，访问defaultdict中的key,若key存在，则返回key对应的value,如果key不存在，就返回默认值。
>
> ```python
> >>> from collections import defaultdict
> >>> d = defaultdict(int)   # 默认的 value 值是 0
> >>> s = 'aaabbc'
> >>> for char in s:
> ...     d[char] += 1
> >>> d
> defaultdict(<type 'int'>, {'a': 3, 'c': 1, 'b': 2})
> >>> d.get('a')
> 3
> >>> d['z']
> 0
> ```

### 函数

#### 装饰器

#### 闭包

### 类

#### 继承多态

#### slots、@property、super和metaclass

### 高级特性

#### 迭代器

#### 生成器

#### 上下文管理器

### 文件处理

#### 正则表达式

### 进程、线程和协程

#### 进程

#### 线程

##### ThreadLocal

#### 协程

### 异常处理

### 模块探究

#### 标准库模块

os、re、base64、hashlib、argpase、datetime

- os



## 参考

[Python之旅](https://funhacks.net/explore-python/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)

[跟老齐学Python](https://github.com/qiwsir/StarterLearningPython)

[极客学院Python教程](http://wiki.jikexueyuan.com/list/python/)

[廖雪峰Python教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/)

[Vamei的Python教程](https://github.com/Vamei/Python-Tutorial-Vamei/tree/master/content)(其中Python标准库--走马观花很不错)