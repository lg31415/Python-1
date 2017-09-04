#!/usr/bin/env python
#-*-coding:utf8-*-

from django.shortcuts import render
from  django.http import HttpResponse

# Create your views here.
'''
    测试
'''
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"


'''
    无参函数
'''
def hello(request):
    return HttpResponse('这是app_welcome的首页!')

if __name__=="__main__":
    hello()
