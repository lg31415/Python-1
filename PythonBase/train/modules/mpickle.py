#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：序列化
'''

try:
    import cPickle as pickle
except ImportError:
    import pickle

def mpickle():
    #字典的构造
    d = dict(name='Bob', age=20, score=88)
    print(d)

    f=open('../data/test.txt','w')
    pickle.dump(d,f)
    f.close()

    f=open('../data/test.txt','r')
    dl=pickle.load(f)
    f.close()
    print(dl)

    f=open('../data/test.txt','r')
    cons=f.read()
    dl1=pickle.loads(cons)
    f.close()
    print(dl1)


if __name__ == "__main__":
    mpickle()
