#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:多线程-生产者消费者模式
    Ref:http://www.toutiao.com/i6466753983980503565/
    State：
    Date:2017/9/21
    Author:tuling56
'''

import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')


import threading
glock=threading.Lock()  # 全局锁


# 全局变量
page_list=['1','2','3','4']
item_list=[] # 共用队列

class Producer(threading.Thread):
    def run(self):
        while len(page_list)>0:
            try:
                glock.acquire()
                page=page_list.pop()
                # do something to item_list using page
            except Exception,e:
                print str(e)
            finally:
                glock.release() # 使用完后要及时释放锁，方便其它线程使用


class Consumer(threading.Thread):
    def run(self):
        while len(item_list)>0:
            try:
                glock.acquire()
                item=item_list.pop()
                # do something to item_list
            except Exception,e:
                print str(e)
            finally:
                glock.release()  #保证锁一定会释放


# 测试入口
if __name__ == "__main__":
    # 两个生产者
    for x in range(2):
        Producer.start() # 类方法

    # 5个消费者，从item_list中取元素进行处理
    for x in range(5):
        Consumer.start()
