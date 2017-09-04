#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:利用zxing进行二维码定位和识别
    Author:tuling56
    参考：https://github.com/oostendo/python-zxing
         http://www.toutiao.com/a6373886387918258433/
    Date:
'''

from zxing import *

zxing_location = "./"  #这里指定的是zxing模块的路径（也即是zxing的包的路径）
testimage = "/home/yjm/Projects/python/pythondev/Projects/qr_scan/samples/samples.png"
drawimage = "/home/yjm/Projects/python/pythondev/Projects/qr_scan/samples/samples.bmp"

'''
  字符串解析
'''
def test_barcode_parser():
  text = """
file:/home/oostendo/Pictures/datamatrix/4-contrastcrop.bmp (format: DATA_MATRIX, type: TEXT):
Raw result:
36MVENBAEEAS04403EB0284ZB
Parsed result:
36MVENBAEEAS04403EB0284ZB
Also, there were 4 result points.
  Point 0: (24.0,18.0)
  Point 1: (21.0,196.0)
  Point 2: (201.0,198.0)
  Point 3: (205.23952,21.0)
"""

  barcode = BarCode(text)
  if (barcode.format != "DATA_MATRIX"):
    return 0

  if (barcode.raw != "36MVENBAEEAS04403EB0284ZB"):
    return 0

  if (barcode.data != "36MVENBAEEAS04403EB0284ZB"):
    return 0

  if (len(barcode.points) != 4 and barcode.points[0][0] != 24.0):
    return 0

  return 1


'''
  条形码识别(基础版)
'''
def test_codereader():
  zx = BarCodeReader(zxing_location)
  #zx = BarCodeReader()

  barcode = zx.decode(testimage)
  print "解析到的数据如下：\n",barcode.data


  if re.match("http://", barcode.data):
    print "解析到网址"
    return 1
  else:
    print "没有解析到网址"

  print "看你还乱不乱"
  return 0

'''
  条形码识别（增强版）
'''
from PIL import Image,ImageDraw
def test_coderead_impl():
   zx = BarCodeReader(zxing_location)
   barcode = zx.decode(testimage)
   ltp=barcode.points[0]
   rdp=barcode.points[0]
   im=Image.open(drawimage)
   dr=ImageDraw.Draw(im)
   dr.rectangle(barcode.points)
   im.show()





# 程序入口
if __name__=="__main__":
  #test_barcode_parser()
  #test_codereader()
  test_coderead_impl()
