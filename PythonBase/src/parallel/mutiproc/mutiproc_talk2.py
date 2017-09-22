#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:进程间通信2-pipe
    Ref:http://www.toutiao.com/i6458130329298272782/
    State：
    Date:2017/9/22
    Author:tuling56
'''

import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

from multiprocessing import Pipe,Process

def proc_send(pipe,what):
    print 'proc_send process %s ...' % (os.getpid())
    s1='hello,I am proc_one,%s' %what
    pipe.send(s1)
    #hues.log('proc_send data is:%s' %s1)


def proc_recv(pipe,f):
    print 'proc_recv process %s ...' % (os.getpid())
    while True:
        hues.log('proc_recv data is:%s' %pipe.recv())
        f.write(pipe.recv())


# 测试入口
if __name__ == "__main__":
    hues.info('Parent process start %s.' % os.getpid())
    f=open('vvv.log','w+')

    pipe=Pipe()
    precv=Process(target=proc_recv,args=(pipe[1],f))
    precv.start()
    for x in xrange(3):
        psend=Process(target=proc_send,args=(pipe[0],str(x)))
        psend.start()
        #psend.join()
    precv.join(6)

    # 关闭接收
    f.close()
    hues.info('Parent process end.')


