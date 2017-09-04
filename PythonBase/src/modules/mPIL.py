#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PIL import Image

def test2():
    Image.open('../../data/bin.png').save('../data/binnew.png')

def test1():
    # 打开含有二维码的图片
    img = Image.open('../../data/bin.png').convert('L')
    #获取图片的尺寸
    width, height = img.size
    raw = img.tostring()

    print raw


if __name__=="__main__":
    test1()



