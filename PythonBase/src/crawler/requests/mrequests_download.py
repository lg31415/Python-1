#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:https://www.zhihu.com/question/41132103
	    https://www.zhihu.com/question/41132103/answer/93438156
	State：
	Date:2017/8/29
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from contextlib import closing

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info())



def main():
    with closing(requests.get("http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3", stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])  # 获取文件的内容
        progress = ProgressBar("razorback", total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        # chunk_size = chunk_size < content_size and chunk_size or content_size
        with open('./file.mp3', "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):  # 迭代获取文件的内容，适合大文件的下载
                file.write(data)
                progress.refresh(count=len(data))


# 测试入口
if __name__ == '__main__':
    main()



