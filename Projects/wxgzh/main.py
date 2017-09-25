# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle

urls = (
    '/wx', 'Handle',
)

'''
class Handle(object):
    def GET(self):
        return "hello, this is a test"
'''

# 测试入口
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
