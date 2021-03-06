#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:Pillow库基本使用
    Ref:http://www.cnblogs.com/apexchu/p/4231041.html
        http://www.th7.cn/Program/Python/201404/193000.shtml
    Date:2016/10/11
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import Image
import numpy as np

def fun():
    im=Image.open("../../data/lena.png")
    print(im.format,im.size,im.mode)

    #格式转换
    imc=im.copy()
    img=imc.convert('L')
    print(img.format,img.size,img.mode)
    img.show()

    # 和numpy对接
    '''
    imb=im.copy()
    imb.thumbnail((25,28))
    #out=imb.point(lambda i:i*1)
    imb_npd=np.asarray(imb,dtype=np.float)
    in_data = np.transpose(imb_npd, (1,0,2))
    imb.show()
    '''

    # 图像粘贴和裁剪
    '''
    imp=im.copy()
    box=(50,50,150,150)
    region=img.crop(box)
    region=region.transpose(Image.ROTATE_180)
    imp.paste(region,box)
    imp.show()
    '''


from PIL import  ImageDraw
def draw():
   points=[(65.0, 112.0), (383.0, 255.0)]
   ltp=points[0]
   rdp=points[0]
   im=Image.open('D:\\samples.bmp')
   dr=ImageDraw.Draw(im)
   dr.rectangle(points,outline=(255,0,0),fill=(0,255,0))
   #im.show()
   im.save("D:\\xx.bmp")


if __name__ == "__main__":
    #fun()
    draw()

