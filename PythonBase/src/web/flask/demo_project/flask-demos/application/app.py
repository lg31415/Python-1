# -*- coding: utf-8 -*-

from flask import Flask, render_template
from controllers import blueprints
from configs import config
from extensions import db, login_manager


# 在app的create_app中进行数据库的初始化，登录的验证、蓝图的注册
def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'  #默认开发配置

    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 读取配置文件

    # db
    db.init_app(app)

    # login
    login_manager.init_app(app)

    # blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    # //该app的handle_error处理
    handle_errors(app)

    return app


def handle_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def acess_forbidden_error(error):
        return render_template('403.html'), 403