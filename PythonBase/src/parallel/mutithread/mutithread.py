#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:多线程
    Ref:http://www.toutiao.com/i6458744258382807565/
        http://www.toutiao.com/i6466753983980503565/
    State：
    Date:2017/9/6
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import time
import threading,random


# 多线程在使用全局变量的时候一定要加锁
t_v=0
lock=threading.Lock()  # 锁初始化

# 其它线程
def run_thread():
    try:
        lock.acquire()
        global t_v
        t_v+=1      # 每个线程都对全局变量t_v的值进行了+1
        time.sleep(random.random())
        hues.info("current thread %s is running.....,value is %s" %(threading.current_thread().name,t_v))
        hues.info("current thread %s end" %(threading.current_thread().name))
    except Exception,e:
        print str(e)
    finally:
        lock.release()  # 保证锁一定会释放

# 主线程
def main_thread():
    hues.success("current thread %s is running" %(threading.current_thread().name))

    t1=threading.Thread(target=run_thread,name='sub_thread1')
    t2=threading.Thread(target=run_thread,name='sub_thread2')
    t3=threading.Thread(target=run_thread,name='sub_thread3')
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

    hues.success("current thread %s end" %(threading.current_thread().name))

# 测试入口
if __name__ == "__main__":
    main_thread()

