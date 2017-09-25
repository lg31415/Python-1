#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:进程通信(Queue实现)
    Ref:https://segmentfault.com/a/1190000008122273
    State：存在的问题是无法保存结果
    Date:2017/8/29
    Author:tuling56
'''
import re, os, sys
import hues
import random

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    进程通信：Queue实现
'''
from multiprocessing import Queue, Process
from Queue import Empty as QueueEmpty
class MutiProcTalkByQueue(object):
    def __init__(self):
        self.f=open('vvv.log','w')

    def __del__(self):
        print "析构了哦"
        self.f.close()

    def _getter(self,name, queue):
        print 'Son process %s' % name
        while True:
            try:
                value = queue.get(True, 5)
                # block为True,就是如果队列中无数据了。
                #   |—————— 若timeout默认是None，那么会一直等待下去。
                #   |—————— 若timeout设置了时间，那么会等待timeout秒后才会抛出QueueEmpty异常
                # block 为False，如果队列中无数据，就抛出QueueEmpty异常
                print "getter get: %f" % value
                self.f.write(str(value)+"\n")
            except QueueEmpty:
                break

    def _putter(self,name, queue):
        print "Son process %s" % name
        for i in range(0, 5):
            value = random.random()
            queue.put(value)
            # 放入数据 put(obj[, block[, timeout]])
            # 若block为True，如队列是满的：
            #  |—————— 若timeout是默认None，那么就会一直等下去
            #  |—————— 若timeout设置了等待时间，那么会等待timeout秒后，如果还是满的，那么就抛出Queue.Full.
            # 若block是False，如果队列满了，直接抛出Queue.Full
            print "putter put: %f" % value

    def proc_talk_queue(self):
        queue = Queue()
        getter_process = Process(target=self._getter, args=("Getter", queue))
        putter_process = Process(target=self._putter, args=("Putter", queue))

        putter_process.join()
        putter_process.start()
        getter_process.start()
        getter_process.join()




# 测试入口
if __name__ == "__main__":
    mbtq=MutiProcTalkByQueue()
    mbtq.proc_talk_queue()

