#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    功能：自定义prometheus的export，将需要检测的数据暴露给prometheus
    参考：https://github.com/prometheus/client_python
'''

import random
import time
from prometheus_client import start_http_server
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''#####################################################
    Summary类型
    列子：统计时间
'''#####################################################
from prometheus_client import  Summary

# Create a metric to track time spent and requests made.(Summary本身是metric的一种)
s = Summary('ttt_summary_request_processing_seconds', 'Time spent processing request')
s.observe(5)

# Decorate function with metric.（计时）
@s.time()
def summary_fun():
    """A dummy function that takes some time."""
    t=random.random()
    time.sleep(t)

'''
    with s.time():
        pass
'''

'''#####################################################
    Counter类型
    例子：异常计数
'''#####################################################
from prometheus_client import Counter
c=Counter('ttt_counter_failures_total', 'Description of counter')
c.inc()

# There are utilities to count exceptions raised:
# 用法1
@c.count_exceptions()   # 这句话的作用是什么？
def counter_fun():
    print "Counter1"
    try:
        intv=int("23xwe")
    except Exception,e:
        c.inc()
    finally:
        time.sleep(5)

# 用法2
'''
def calc_exception():
    # count all exception
    with c.count_exceptions():
        print "exception +1"
        time.sleep(5)
        c.inc()

    # Count only one type of exception
    with c.count_exceptions(ValueError):
        pass
'''


'''#####################################################
    Gauge类型
    例子：异常计数
'''#####################################################
from prometheus_client import Gauge
g = Gauge('ttt_gauge_inprogress_requests', 'Description of gauge')
g.inc()      # Increment by 1
g.dec(10)    # Decrement by given value
g.set(4.2)   # Set to a given value
#g.set_to_current_time()   # Set to current unixtime

@g.track_inprogress()
def gauge_fun():
    print "Guage1"
    time.sleep(5)
    #g.inc(10)

'''
    with g.track_inprogress():
        pass
'''
d = Gauge('ttt_gauge_data_objects', 'Number of objects')
my_dict = {}

def gauge_fun2():
    print "Guage2"
    i=random.random()
    my_dict[i]=i
    d.set_function(lambda: len(my_dict))


'''########################################################
    Histogram类型
'''########################################################
from prometheus_client import Histogram
h = Histogram('ttt_historgram_request_latency_seconds', 'Description of histogram')
h.observe(4.7)    # Observe 4.7 (seconds in this case)

@h.time()
def historgram_fun():
    print "histogram"
    t=random.random()
    time.sleep(t)



'''#####################################################
    Labels类型(配合其它类型使用)
'''#####################################################
#from prometheus_client import Counter
cl = Counter('ttt_labels_requests_total', 'HTTP Failures', ['method', 'endpoint'])

def labels_fun():
    print "labels"
    cl.labels('get', '/').inc()
    cl.labels('post', '/submit').inc()
    #cl.labels(method='get', endpoint='/').inc()
    #cl.labels(method='post', endpoint='/submit').inc()




'''#####################################################
    主程序入口
'''
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(3003)

    i=0
    while True:
        time.sleep(5)
        t=random.random()
        print '===============run+1======================'

        # summary
        summary_fun()

        # counter
        counter_fun()

        # gauge
        gauge_fun()
        gauge_fun2()

        #histogram
        historgram_fun()

        #labels
        labels_fun()




