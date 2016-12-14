# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python数据操作
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#序列化操作（一维不同质可变长数组）
def mplot():
    ldata=[1,2,7,3,8,4,5,5,6,10]
    ndata=np.array(ldata)
    plt.plot(ndata,np.sin(ndata),'--',linewidth=2,color='red')
    plt.show()

    x=[1,2,5,3,42,1,5]
    y=[1,23,34,3,54,64,1]
    plt.figure
    plt.plot(x,'o')
    plt.show()


if __name__ == "__main__":
    mplot()
