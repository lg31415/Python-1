#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yjm'
'''
    Fun:系统状态获取和监测模块
    Ref:http://www.toutiao.com/a6344685980779806978/
    State：ing...，后期可以和Echars进行整合，图形化显示
    Date:2016/10/24
    Author:tuling56
'''

import os
import sys
import datetime
import psutil
import socket

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    获取当前系统转台信息
'''
class MonitorOS():
    def __init__(self):
        self.hostname=socket.gethostname()  #获取主机名

    # 获取CPU信息
    def get_cpu(self):
        info = psutil.cpu_times()
        res = dict(
            user=info.user,                           # 执行用户进程的时间百分比
            system=info.system,                       # 执行内核进程和中断的时间百分比
            iowait=info.iowait,                       # 由于IO等待而使CPU处于idle(空闲)状态的时间百分比
            idle=info.idle,                           # CPU处于idle状态的时间百分比
            cpucount1=psutil.cpu_count(),               # 获取CPU的逻辑个数
            cpucount2=psutil.cpu_count(logical=False) # 获取CPU的物理个数
            )
        print res

    # 获取进程信息（列出的是每个进程的信息字典）
    def get_proc(self):
        pidsinfo = psutil.pids()                             # 列出所有进程pid
        pinfo = map(lambda v: psutil.Process(v), pidsinfo)  # 实例化进程状态
        res = dict(
            pinfo=[
                dict(
                    pid=v[0],                 # 进程pid
                    name=v[1].name(),         # 进程名称
                    exe=v[1].exe(),         # 进程bin路径
                    cwd=v[1].cwd(),         # 进程工作目录绝对路径
                    status=v[1].status(),   # 进程状态
                    create_time=datetime.datetime.fromtimestamp(v[1].create_time()).strftime("%Y-%m-%d %H:%M:%S"),    # 进程创建时间

                    uids=dict(
                        real=v[1].uids().real,
                        effective=v[1].uids().effective,
                        saved=v[1].uids().saved,
                    ), # 进程uid信息

                    gids=dict(
                        real=v[1].gids().real,
                        effective=v[1].gids().effective,
                        saved=v[1].gids().saved,
                    ), # 进程gid信息

                    cpu_times=dict(
                        user=v[1].cpu_times().user,                     # 用户cpu时间
                        system=v[1].cpu_times().system,                 # 系统cpu时间
                    ), # 进程cpu时间

                    cpu_affinity=v[1].cpu_affinity(),                     # 进程cpu亲和度
                    memory_percent=round(v[1].memory_percent(), 2),     # 进程内存利用率

                    memory_info=dict(
                        rss=v[1].memory_info().rss,                     # 进程内存rss信息
                        vms=v[1].memory_info().vms                         # 进程内存vms信息
                    ), # 进程内存信息

                    io_counters=dict(
                        read_count=v[1].io_counters().read_count,         # 读IO数
                        write_count=v[1].io_counters().write_count,     # 写IO数
                        read_bytes=v[1].io_counters().read_bytes,         # IO读字节数
                        write_bytes=v[1].io_counters().write_bytes,     # IO写字节数
                    ), # 进程IO信息
                    num_threads=v[1].num_threads(),                     # 进程开启的线程数
                    # connections = v[1].connections()                    # 打开进程socket的namedutples列表
                )
                for v in zip(pidsinfo, pinfo)
            ]
        )
        res["pinfo"] = sorted(res["pinfo"], key=lambda v: v["memory_percent"], reverse=True)
        print res

    # 获取内存信息
    def get_mem(self):
        meminfo = psutil.virtual_memory()
        swapinfo = psutil.swap_memory()
        res = dict(
            mem_gb=dict(
                total=round(meminfo.total / (1024 ** 3.0), 2),          # 内存总数
                available=round(meminfo.available / (1024 ** 3.0), 2), # 可用内存数
                percent=meminfo.percent,
                used=round(meminfo.used / (1024 ** 3.0), 2),             # 已使用的内存数
                free=round(meminfo.free / (1024 ** 3.0), 2),             # 空闲内存数
                active=round(meminfo.active / (1024 ** 3.0), 2),         # 活跃内存数
                inactive=round(meminfo.inactive / (1024 ** 3.0), 2),  # 不活跃内存数
                buffers=round(meminfo.buffers / (1024 ** 3.0), 2),     # 缓冲使用数
                cached=round(meminfo.cached / (1024 ** 3.0), 2),         # 缓存使用数
                shared=round(meminfo.shared / (1024 ** 3.0), 2)         # 共享内存数
            ),
            swap_gb=dict(
                total=round(swapinfo.total / (1024 ** 3), 2),         # 交换分区总数
                used=round(swapinfo.used / (1024 ** 3), 2),         # 已使用的交换分区数
                free=round(swapinfo.free / (1024 ** 3), 2),         # 空闲交换分区数
                percent=swapinfo.percent,
                sin=round(swapinfo.sin / (1024 ** 3), 2),             # 输入数
                sout=round(swapinfo.sout / (1024 ** 3), 2)             # 输出数
            )
        )
        print res

    # 获取网络信息
    def get_net(self):
        allnetio = psutil.net_io_counters()            # 获取网络总的IO信息
        onenetio = psutil.net_io_counters(pernic=True) # 输出每个网络接口的IO信息
        res = dict(
            allnetio=dict(
                bytes_sent=allnetio.bytes_sent,     # 发送字节数
                bytes_recv=allnetio.bytes_recv,     # 接受字节数
                packets_sent=allnetio.packets_sent, # 发送数据包数
                packets_recv=allnetio.packets_recv, # 接受数据包数
                errin=allnetio.errin,
                errout=allnetio.errout,
                dropin=allnetio.dropin,
                dropout=allnetio.dropout
            ),
            onenetio=[
                dict(
                    name=v[0],
                    bytes_sent=v[1].bytes_sent,     # 发送字节数
                    bytes_recv=v[1].bytes_recv,     # 接受字节数
                    packets_sent=v[1].packets_sent, # 发送数据包数
                    packets_recv=v[1].packets_recv, # 接受数据包数
                    errin=v[1].errin,
                    errout=v[1].errout,
                    dropin=v[1].dropin,
                    dropout=v[1].dropout
            )
            for v in onenetio.iteritems()
            ]
        )
        print res

    # 获取登录用户信息
    def get_user(self):
        usersinfo = psutil.users() # 当前登录系统的用户信息
        res = dict(
            usersinfo=[
                dict(
                    name=v.name,          # 当前登录用户名
                    terminal=v.terminal, # 打开终端
                    host=v.host,          # 登录IP地址
                    started=datetime.datetime.fromtimestamp(v.started).strftime("%Y-%m-%d %H:%M:%S") # 登录时间
                )
                for v in usersinfo
            ],
            boottime=datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") # 开机时间
        )
        print res

    # 获取磁盘信息
    def get_disk(self):
        partinfo = psutil.disk_usage("/") #获取磁盘完整信息
        diskinfo = dict(
            free=round(partinfo.free / (1024 ** 3), 2), #磁盘剩余量
            used=round(partinfo.used / (1024 ** 3), 2), #磁盘使用量
            total=round(partinfo.total / (1024 ** 3), 2),#磁盘总量
        )
        print(diskinfo)


'''
    测试入口
'''
if __name__ == "__main__":
    mos=MonitorOS()
    #mos.get_cpu()
    #mos.get_mem()
    #mos.get_net()
    #mos.get_disk()
    mos.get_proc()
    #mos.get_user()

