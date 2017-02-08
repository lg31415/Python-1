#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：python利用pickle和cPickle进行序列化和反序列化
'''
try:
    import cPickle as pickle
except:
    import pickle

def mpicke():
    # 序列化
    d={'zhang':24,'wang':12,'lizhang':45}
    dstr=pickle.dumps(d)
    f=open('dstr.txt','w')
    f.write(dstr)
    f.close()

    #反序列化
    f1=open('dstr.txt','r')
    content=f1.read()
    f1.close()
    dr=pickle.loads(content)
    print dr

if __name__ == "__main__":
    mpicke()
