## 并行处理技术

[TOC]

前言：

> 并行处理技术这里指的是Python多进程和多线程学习笔记，实现多任务的方式有以下几种：
>
> - 多进程模式
> - 多线程模式（在一个进程中开启多个线程）
> - 多进程+多线程

### 多进程

python的os模块封装了常见的系统调用，我们可以在linux和mac上通过`fork`操作实现进程的创建，但是windows上没有fork调用，可以通过mutiprocessing模块的`Process`类来实现多进程

#### 创建多进程

Process类的构造方法：

- 构造方法__init__(self, group=None, target=None, args=(), name=None, kwargs={})
- 参数说明：
  - group：进程所属组。基本不用
  - target：表示调用对象或方法名称。
  - args：表示调用对象的位置参数元组。
  - name：别名
  - kwargs：表示调用对象的字典。

```python
import os

```



#### 多进程通信

#### 多进程管理

##### 进程池Pool

Pool的概念如何理解

### 多线程

#### 创建多线程

#### 线程之间同步（锁的使用）



## 参考

[python进程系列的学习笔记](https://segmentfault.com/u/charliecharlie/articles?page=1)

[趣文:我是一个线程](http://blog.jobbole.com/99883/)（推荐）

[趣文:以生活例子来说明多进程和多线程](http://mp.weixin.qq.com/s?__biz=MjM5OTMxMzA4NQ==&mid=2655932144&idx=1&sn=2f6a122d5e0363f2dbb85fc2b7e406cd&scene=0#rd)（推荐）

[Python使用Pipe和Queue进程间通信](https://segmentfault.com/a/1190000008122273)

[今日头条:Python多进程学习（系列）](http://www.toutiao.com/i6457730350452834829/)

[Python多进程并发实例讲解（推荐）](http://www.jb51.net/article/67116.htm)

