# -*- coding: utf-8 -*-

from app import create_app
from app import db

#定义了可以在from <module> import * 中使用的符合
__all__ = ['create_app', 'db']
