#!/usr/bin/env python 
#-*-conding:utf8-*-

from django.shortcuts import render
from  django.http import HttpResponse

# Create your views here.

def hello(request):
    return HttpResponse("hello,this is content_welcome app!")

