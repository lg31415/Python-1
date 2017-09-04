#-*- coding:utf-8 -*-
from django.db import models

# 这里定义数据模型
# Create your models here.
class DBO(models.Model):
    name=models.CharField(max_length=20,unique=True)
    age=models.IntegerField(max_length=10)

class Wiki(models.Model):
    pagename = models.CharField(max_length=20, unique=True)
    content = models.TextField()