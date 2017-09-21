## Python学习笔记

[TOC]

### 数据类型

#### 基础类型

##### 列表（元组）

##### 集合

##### 字典



#### 标准库模块

##### 赋值、深拷贝和潜拷贝

```python
#  赋值传递的是对象的引用，原始列表改变，被赋值的变量也会做相同的改变
#  浅拷贝：只拷贝了不可变对象，可变对象的值是引用
#  深拷贝：包含对象里面的自对象的拷贝，所以原始对象的改变不会造成深拷贝里任何子元素的改变
  
```

**参考**

[python的赋值、深拷贝和潜拷贝](http://www.toutiao.com/i6386988193475985921/)

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

在不改变函数本身的情况下，使得函数的调用和返回发生变化，几个关键点：

- 函数可以作为变量
- 函数可以传递给函数
- 函数嵌套函数

装饰器的核心就是将函数作为参数传递给另一个函数

```python
@decrator
def func():
	pass
```

举例：

```python
# 定义一个嵌套函数，分别以函数和普通的字符串作为参数
def add_tag(func):
    def prt_func(name):
        return '<p>{0}</p>'.format(func(name))    
    return prt_func
# 定义一个普通的函数,并调用装饰器

@add_tag
def print_text(name):
    return 'hello,'+ name

print(print_text('crossin'))
# 结果 : <p>hello,crossin</p>
```

#### 闭包

在定义函数时候，再嵌套定义一个函数，并将该嵌套函数返回,闭包是装饰器的特殊实例。

```python
from math import pow

def make_pow(n):
    def inner_func(x):     # 嵌套定义了 inner_func
        return pow(x, n)   # 注意这里引用了外部函数的 n
    return inner_func      # 返回 inner_func
```

返回的内部函数引用了外部函数的相关参数和变量，我们把该返回的内部函数称为闭包。

- 闭包的最大特点是引用了自由变量，即使生成闭包的环境已经释放，闭包依然存在。
- 闭包在运行时可以有多个实例，即使传入的参数相同
- 利用闭包可以模拟类的实例
- 尽量避免在闭包中引用循环变量，或者后续会发生变化的量





#### 高阶函数

可接受其他函数作为参数的函数称为高阶函数。

```python
# 高阶函数
def func(g,arr)
	return [g(x) for x in arr]

def double(x):
    return 2*x

# 调用高阶函数
arrres=func(double,[1,2,3,4])
```

##### map/reduce/filter

> map/reduce/filter作为高阶函数的代表

```python
# map
map(function,sequence)
## 对序列中的item依次执行function（item）,并将结果组成一个list返回,其中item元素也可以是函数对象，如下：
value=list(map(lambda f:f(4),[double,triple,square]))

# reduce
reduce(function, sequence[, initial])
## 解释：先将 sequence 的前两个 item 传给 function，即 function(item1, item2)，函数的返回值和 sequence 的下一个 item 再传给 function，即 function(function(item1, item2), item3)，如此迭代，直到 sequence 没有元素，如果有 initial，则作为初始值调用。

# filter
filter(function, sequnce)
## 依次作用于sequence的每个item,甲方那个返回值为True的item组成一个List/String/Tuple (取决于 sequnce 的类型，python3 统一返回迭代器) 返回。
```

##### 匿名函数

> lambda函数一般用于创建一些临时性的，小巧的函数,匿名函数本质上是一个函数，没有函数名称。

```python
arr = func(lambda x: x + 1, [1, 2, 3, 4])
```

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

##### 多进程创建

##### 多进程通信

mutiprocessing.Pipe()单双工通信

![单双工通信](https://segmentfault.com/img/bVIeWr?w=960&h=540)

mutiprocessing.Queue()

#### 线程

##### ThreadLocal

#### 协程

### 异常处理

### 模块探究

#### 标准库模块

os、re、base64、hashlib、argpase、datetime

- os


### 常见问题

#### 编码

```python
#coding = utf-8


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
```



## 参考

[Python之旅](https://funhacks.net/explore-python/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)

[跟老齐学Python](https://github.com/qiwsir/StarterLearningPython)

[极客学院Python教程](http://wiki.jikexueyuan.com/list/python/)

[廖雪峰Python教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/)

[Vamei的Python教程](https://github.com/Vamei/Python-Tutorial-Vamei/tree/master/content)(其中Python标准库--走马观花很不错)

[Python修改path的搜索路径](http://blog.csdn.net/gqtcgq/article/details/49365933)