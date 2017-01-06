#!/bin/python
# -*-coding:utf8-*-

from prometheus_client import Gauge
from prometheus_client import start_http_server

import threading 
import json
import requests
import time
import sys
import os


data={"points":[[1,2,3,4,5,6],[1,2,3,4,5,6]]}
service_name="mexporter"


'''
	定时采集制定查询规则和结果数据返回
	状态：待完成
'''
def alauda_get_instance_metrics(namespace, name, instance_uuid, start_time, end_time, interval):
    pass


'''
	数据收集
'''
def gather_data(namespace, run_event):
    g_cpu_usage = Gauge("cpu_cumulative_usage", "CPU Cumulative Usage", ["service", "instance"])
    g_cpu_utilization = Gauge('cpu_utilization', "CPU utilization", ["service", "instance"])
    g_memory_usage = Gauge('memory_usage', "Memory Usage", ["servie", "instance"])
    g_memory_utilization = Gauge('memory_utilization', "Memory Utilization", ["service", "instance"])

    while run_event.is_set():
        if data:
            g_cpu_usage.labels(service_name, "exporter_service").set(data['points'][0][1])
            g_cpu_utilization.labels(service_name, "exporter_service").set(data['points'][0][2])
            g_memory_usage.labels(service_name, "exporter_service").set(data['points'][0][3])
            g_memory_utilization.labels(service_name, "exporter_service").set(data['points'][0][4])
        time.sleep(20)

if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()

    thread = threading.Thread(target=gather_data, args=('darkheaven', run_event))
    thread.start()

    try:
        start_http_server(9104)
        while True:
            print "休眠失眠后启动web服务"
            time.sleep(10)

    except KeyboardInterrupt:
        run_event.clear()
        thread.join()
        sys.exit(0)
    except:
        sys.exit(1)
