## Python程序打包移植方法

---

**问题描述：**

本地开发环境需要某一个库，如何将程序移植到另一台机器上，而这台机器不需要在配置和我的开发环境相同的包，（java里有maven可以方便的打成jar包进行部署）

**赞成**

> 方便小白使用

**反对**

> python的一些库内部使用的是C语言，C 语言的，使用 easy_install/pip 安装的时候，往往是下载源码然后本机编译的。如果打包了，可能会出现一些莫名奇妙的问题，比如 32、64 位的兼容问题，不同的操作系统的路径查找问题，等等。
>
> > 正确的方式就是在 setup.py 文件中写明依赖的库和版本，然后到目标机器上安装，反正就一句 python setup.py install，不算复杂

**最简单的实现方式：**

```shell
- 使用 pip freeze > requirements.txt 导出需要的包和对应的版本
- 在移植机器上使用pip install -r requirements.txt 安装对应版本的依赖包
(注意筛选掉不需要的包，pip freeze 导出了所有安装的包)
```

**实现方法**

1. setuptools
2. buildout
3. wheels

---

### 安装包

#### setuptools实现方式

setuptools是python的模块打包工具

> setup.py文件改怎么写？
>
> ```
> 在setup.py里描述依赖的包，当调用`python setup.py install`的时候，就会自动包所有依赖包都装好
> ```
>
> 模块安装方式：
>
> - 单文件模块：直接拷贝到安装的库目录里即可
>
> - 多文件模块：setup.py[^编写]:
>
>   [^编写]: 没有解决依赖项的问题啊
>
>   ​

##### setup.py文件写法

- setup.py样例

```python
# ###样例1
#!/bin/env python
#-*-coding:utf8-*-
from setuptools import setup, find_packages
setup(
      name="mytest",				#打包后的包文件名
      version="0.10",
      description="My test module",
      author="Robin Hood",
      url="http://www.csdn.net",
      license="LGPL",
      packages= find_packages(),
      scripts=["scripts/test.py"],  #表示将该文件放到python的Scripts目录下
 )

# ###样例2
#!/bin/env python
#-*-coding:utf8-*-
from distutils.core import setup   #（和样例1有点不一样）
from setuptools import find_packages
setup(
	  name='MyTs',  
      version='1.0',
      description='My Blog Distribution Utilities',
	  license="LGPL",
	  platforms='Unix',
      author='Liu tiansi',
      author_email='liutiansi@gmail.com',
      url='http://blog.liuts.com',
	  packages=find_packages(),            # ['.'],   # 需要打包的目录列表
      py_modules=['test','test1'],         # 需要打包的python文件列表
	  requires=['numpy>=1.6'],             # 依赖的包
	  provides=['test','test1'],		   # 提供的包
	  data_files=[],					   # 打包时需要打包的数据文件，如图片，配置文件等
	  scripts=['']						   # 安装时需要执行的脚本列表
)
```

​	其中test.py的内日如下:`print "show me"`

##### setup.py的打包

- setpy.py打包时的配置参数

  ```shell
  >>python setup.py --help
    --name              包名称
    --version (-V)      包版本
    --author            程序的作者
    --author_email      程序的作者的邮箱地址
    --maintainer        维护者
    --maintainer_email  维护者的邮箱地址
    --url               程序的官网地址
    --license           程序的授权信息
    --description       程序的简单描述
    --long_description  程序的详细描述
    --platforms         程序适用的软件平台列表
    --classifiers       程序的所属分类列表
    --keywords          程序的关键字列表
    --packages  		  需要打包的目录列表
    --py_modules  	  需要打包的python文件列表
    --download_url  	  程序的下载地址
    --cmdclass  
    --data_files  	  打包时需要打包的数据文件，如图片，配置文件等
    --scripts  		  安装时需要执行的脚步列表
  ```

  ​


- python setup.py sdist   #打包后的格式为tar.gz/zip

  ```shell
  setup.py的打包参数：
  % python setup.py build 	 	#编译
  % python setup.py install   	#安装
  % python setup.py sdist      	#制作分发包格式为tar.gz/zip
  % python setup.py bdist_wininst #制作windows下的exe分发包
  % python setup.py bdist_rpm     #生成Linux下的rpm分发包
  % python setup.py bdist_egg     #生成安装信息（但不进行安装）
  ```

  ​

- 运行结果:

  > 在当前目录下新增dist目录，有个同名的压缩包，windows下是zip,linux下是tar.gz

##### setup.py包的安装

安装测试

> 解压刚才打包好的文件，运行python setup.py install，然后进入python环境，执行import test命令
>
> setup.py的安装参数：

#### buildout实现方式

> 只需要写一个buildout.cfg文件就可以了，然后给别人

#### wheels实现方式

> 用 Python Wheels 可以把依赖项打包到一个 .whl 文件里。
>
> [Python Wheels](https://link.zhihu.com/?target=http%3A//pythonwheels.com/)
>
> 

**wheels方法的优点:**

1. Faster installation for pure python and native C extension packages.
2. Avoids arbitrary code execution for installation. (Avoids setup.py)
3. Installation of a C extension does not require a compiler on Windows or OS X.
4. Allows better caching for testing and continuous integration.
5. Creates .pyc files as part of installation to ensure they match the python interpreter used.
6. More consistent installs across platforms and machines.

### 引用包

python模块的每一个包中都有一个`__init__.py`的文件，该文件定义了包的属性和方法，然后是一些模块文件和子目录，如果子目录中也有`__init__.py` ,则是包的子包，模块引入的时候实际上是导入了它的`__init__.py`文件。



### 参考

​	[python 如何连同依赖打包发布以及python的构建工具？](https://www.zhihu.com/question/21639330)

- setup.py

  [如何使用和制作 Python 安装模块-setuptools](http://blog.csdn.net/ponder008/article/details/6592719)

   [python模块的打包-setuptools](http://blog.csdn.net/five3/article/details/7847551)

  [Python包管理工具setuptools详解](http://www.360doc.com/content/14/0306/11/13084517_358166737.shtml)(解决了模块包含问题)

- buildout

- wheels

----

## Python程序移植到Windows平台

`py2exe`将python脚本转换成在windows上可独立直线的.exe程序，这样可以在windows上直接运行这个可执行程序，而不需要安装python环境和相应的开发包

### 进度

这个部分暂时搁置了，很长时间都没有什么进展

### 参考

[python打包成exe的方法](http://www.cnblogs.com/whiteyun/archive/2009/09/28/1575526.html)

---

## Python程序以Linux服务部署

>  整体思路是将python程序进行封装，设置开机自动启动形式，也可以在crontab里设置定时执行，*服务的本质是一种一直在运行的程序*，python程序如何监听端口，调用这个程序，传递参数，实现通信。

### 单独的可执行文件部署

- 编写程序

- 在/etc/init.d/中创建服务xx_service,格式如下:

  ```
  #! /bin/sh
  # chkconfig: - 85 15    
  # description: nginx is a World Wide Web server. It is used to serve

  # Default-Start:     2 3 4 5
  # Default-Stop:      0 1 6
  # Short-Description: starts the nginx web server

  -----后面还有很多参数要配置的------
  ```

  尤其注意第二行，必须添加，不然会报`service myservice does not support chkconfig` 错误

- 添加服务: chkconfig --add xx_service

  > 删除服务：chkconfig --del xx_service

- 设置服务启动级别

  >   chkconfig --level 35 xx_service  on 
  >
  > :grey_question:启动级别分别对应什么

```
利用service python_service start(status)启动后的结果如下：
进程启动关系有点乱：
root      2288  1495  0 21:05 pts/0    00:00:00 /bin/sh /usr/sbin/service python_service start
root      2298  2288  0 21:05 pts/0    00:00:00 /bin/bash /etc/init.d/python_service start
root      2299  2298  0 21:05 pts/0    00:00:00 /usr/bin/python /home/yjm/Projects/pythonservice/python_service.py

而且，开启启动这个服务后，无法停止，只能杀死所有相关进程才能停止，这部分可以参考nginx服务启动脚本的编写方法
```

### 以后台服务的接口实现

利用uwsgi作为网关，将接口用python来实现

### 参考

[将python程序以linux服务部署](http://blog.csdn.net/philip502/article/details/13511625)

