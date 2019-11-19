# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# p143 sqlite数据库URI在不同系统下斜杆数量不同
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # 从环境变量中读取，如果没有，使用默认值 dev key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False  # Flask-DebugToolbar 是否拦截重定向

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # p143 配置变量决定是否追踪对象，建议关闭
    SQLALCHEMY_RECORD_QUERIES = True  # 可以用于显式地禁用或者启用查询记录

    # 开启CSRF protection
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # p179 配置flask-mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')  # 用于发送邮件的smtp服务器
    # MAIL_PORT = 465  # 发信端口
    # MAIL_USE_SSL = True  # SSL加密
    MAIL_PORT = 587  # 发信端口
    MAIL_USE_TLS = True  # TLS 加密
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # 发信服务器用户名
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # 发信服务器密码

    # MAIL_DEFAULT_SENDER = ('Breakblog Admin', MAIL_USERNAME)  # p181 默认发信人
    MAIL_DEFAULT_SENDER = 'Breakblog Admin <tw.huang@breakblog.me>'

    BREAKBLOG_EMAIL = os.getenv('BREAKBLOG_EMAIL')  # 网站管理员收件人邮箱地址

    BREAKBLOG_POST_PER_PAGE = 10  # 每页面文章的数量
    BREAKBLOG_COMMENT_PER_PAGE = 15  # 每页评论列表数量
    BREAKBLOG_MANAGE_POST_PER_PAGE = 15  # p285 后台显示管理每页文章的数量

    # ('theme name', 'display name') # 更换主题 p269
    # BREAKBLOG_THEMES = {'simplex': 'Simplex', 'darkly': 'Darkly'}

    BREAKBLOG_SLOW_QUERY_THRESHOLD = 1

    BREAKBLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')  # 上传路径
    BREAKBLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    # https://github.com/greyli/flask-ckeditor
    CKEDITOR_HEIGHT = 360  # 配置ckeditor插件


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
