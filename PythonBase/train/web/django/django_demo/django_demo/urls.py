#-*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from django_1 import views

# 这里配置url访问的方式
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello$',views.hello),
    url(r'^add/',views.add),
    url(r'^address',views.addressbook),
    url(r'csv/(?P<filename>\w+)/$',views.output),   #添加此句

    url(r'^wiki/$',views.index),
    url(r'^wiki/(?P<pagename>\w+)/$',views.index),
    url(r'^wiki/(?P<pagename>\w+)/edit/$',views.edit),
    url(r'^wiki/(?P<pagename>\w+)/save/$',views.save)
    )
