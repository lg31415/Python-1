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

'''
    Summary
'''

'''
from prometheus_client import  Summary

# Create a metric to track time spent and requests made.(Summary本身是metric的一种)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.（计时）
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)
'''


'''
    Counter
    例子：异常计数
'''

from prometheus_client import Counter
c=Counter('my_failures_total', 'Description of counter')
c.inc()

@c.count_exceptions()
def counter_fun(v1):
    try:
        intv=int(v1)
    except Exception,e:
        pass
    finally:
        time.sleep(5)

'''
def calc_exception():
    with c.count_exceptions():
        print "exception +1"
        time.sleep(5)
'''

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        #process_request(random.random())
        print "run+1"
        counter_fun("23xwe")

