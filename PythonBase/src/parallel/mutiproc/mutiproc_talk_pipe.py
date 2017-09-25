#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:进程间通信2-pipe
    Ref:http://www.toutiao.com/i6458130329298272782/
    State：存在的问题是无法保存结果
    Date:2017/9/22
    Author:tuling56
'''

import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

from multiprocessing import Pipe,Process

#f=open('vvv.log','w+')

def proc_send(pipe,what):
    print 'proc_send process %s ...' % (os.getpid())
    s1='hello,I am proc_one,%s' %what
    pipe.send(s1)
    #hues.log('proc_send data is:%s' %s1)


def proc_recv(pipe):#,f):
    #global f
    print 'proc_recv process %s ...' % (os.getpid())
    while True:
        try:
            hues.log('proc_recv data is:%s' %pipe.recv())
            #f.write(pipe.recv())
        except EOFError:
            # 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程
            print u"子进程退出"
            break


# 测试入口
if __name__ == "__main__":
    hues.info('Parent process start %s.' % os.getpid())
    in_pipe,out_pipe=Pipe()
    precv=Process(target=proc_recv,args=(out_pipe,))
    precv.start()

    for x in xrange(3):
        psend=Process(target=proc_send,args=(in_pipe,str(x)))
        psend.start()
        psend.join()
    precv.join(6)

    # 关闭接收
    #f.close()
    hues.info('Parent process end.')


