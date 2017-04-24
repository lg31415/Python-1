# -*- coding: utf-8 -*-

# //使用到了以下两个扩展：数据库扩展和登录扩展
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# db
db = SQLAlchemy()

# login_manager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
