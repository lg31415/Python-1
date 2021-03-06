# 二维码识别方案

[TOC]
## zbar解决方案

### 安装

#### 安装依赖项

> yum install ImageMagick ImageMagick-devel

#### 安装zbar
>方法1：编译安装
>
>
> > wget http://ncu.dl.sourceforge.net/project/zbar/zbar/0.10/zbar-0.10.tar.bz2
> >
> > tar -jxvf  zbar-0.10.tar.bz2
> >
> > ./configure --without-gtk --without-qt --disable-video --prefix=/usr/local
> >
> > ```
> > 注意关闭：video支持，否则报警：
> > configure: error: test for video support failed!
> > rebuild your kernel to include video4linux support or
> > configure --disable-video to skip building video support.
> > ```
> >
>
>方法2：直接yum安装
>
>> yum install zbar zbar-devel
>
#### 安装python的zbar包
>
> > wget https://pypi.python.org/packages/c8/ee/9a2dee14943c56520faf059914b815729ac6a732c8e608b24c0cad197238/zbar-0.10.zip
> >
> > python setup.py install

依赖关系说明:python的zbar包是不能直接进行二维码识别的，只能调用zbar的可执行文件来进行识别，所以需要先安装zbar。

```mermaid
graph LR
zbar-->|依赖|python_zbar
```

### 测试

> ```python
> #!/usr/bin/env python
> # -*- coding:utf-8 -*-
> import zbar
> from PIL import Image
> # 创建图片扫描对象
> scanner = zbar.ImageScanner()
> # 设置对象属性 
> scanner.parse_config('enable')
> # 打开含有二维码的图片(注意是bmp格式的，其它格式的需要安装对应的包支持)
> img = Image.open('qr.bmp').convert('L')
> #获取图片的尺寸
> width, height = img.size
> raw = img.tostring() 
> #建立zbar图片对象并扫描转换为字节信息
> qrCode = zbar.Image(width, height, 'Y800', raw)
> scanner.scan(qrCode)
> data = '' 
> for s in qrCode: data += s.data
> # 删除图片对象
> del img
> # 输出解码结果
> print data
> ```

### 参考

[python解析二维码](http://www.toutiao.com/a6355324610682978561/)

[python 使用zbar解码二维码](http://blog.csdn.net/kkxgx/article/details/7749319)

## zxing解决方案

​	zbar不能识别倾斜的条形码，而且也不能都能够为条形码区域，而[ZXing](https://github.com/zxing/zxing)则更加强大。[python zxing包](https://github.com/oostendo/python-zxing)的描述为 a quick and dirty wrapper for the ZXing barcode library.（一个快速且简陋的zxing外壳）

需要说明的是的python的zxing包只是基于ZXing库的一个外壳，ZXing库本身是Java编写的,此外还有其他的cpp,ruby,js等外壳。

例子：

```python
from zxing import *

zxing_location = "./"  #这里指定的是zxing模块的路径（也即是zxing的包的路径,默认是父目录）

def test_codereader():
  zx = BarCodeReader(zxing_location)
  #zx = BarCodeReader()

  barcode = zx.decode(testimage)
  print "解析到的数据如下：\n",barcode.data
```

说明：

- zxing目录下的ZXing.py是分离出来的模块包，使用方法如下：

```python
from Zxing import *
# 取代(避免安装)
from zxing import *
```

- core.jar,javase.jar,jcommender-1.48.jar

这个是ZXing库的编译之后的jar包





