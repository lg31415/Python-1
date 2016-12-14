#-*-coding:utf-8-*-
import cv2
import numpy
import os

#make an array of 120,000 random bytes
randomByteArray=bytearray(os.urandom(120000))
#转化为numpy数组
flatNumpyArray=numpy.array(randomByteArray)
#构造灰度图
grayimg=flatNumpyArray.reshape(300,400)
cv2.imwrite('randomGray.jpg',grayimg)

#构造彩色图
bgrimg=flatNumpyArray.reshape(100,400,3)
cv2.imwrite("randomColor.jpg",bgrimg)

#实验
colorimg=cv2.imread('baidu.jpg') #该图像的原始尺寸是(width,height)->(742,217)
colorarray=bytearray(colorimg)
print  len(colorarray), type(colorarray)
colorNumpyArray=numpy.array(colorarray)
print  type(colorNumpyArray)

recon_colorimg=colorNumpyArray.reshape(742,217,3) #reshape的第一个参数是矩阵的函数，对应着图像的高
cv2.imwrite("baidu_reconstruct.jpg",recon_colorimg)

#读取一个灰度图，查看是否真的是安装彩色格式读取的
imgread=cv2.imread('gray.jpg',cv2.CV_LOAD_IMAGE_GRAYSCALE)
print  'over'
