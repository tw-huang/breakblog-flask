# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

import click
from flask import Flask, request, render_template
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from breakblog.blueprints.admin import admin_bp
from breakblog.blueprints.auth import auth_bp
from breakblog.blueprints.blog import blog_bp
from breakblog.extensions import bootstrap, db, moment, csrf, ckeditor, login_manager, mail, toolbar, migrate

from breakblog.models import Admin, Category, Post, Comment, Link
from breakblog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# 定义工厂函数create_app()
def create_app(config_name=None):
    if config_name is None:
        # p228先从.flaskenv 文件中获取，没有获取使用默认值development
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('breakblog')
    app.config.from_object(config[config_name])  # 从settings.py中导入配置文件

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册自定义shell命令
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_template_context(app)  # 注册模板上下文处理函数
    register_request_handlers(app)  # 注册请求上下文处理函数
    return app


# 注册日志处理器
def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/breakblog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Breakblog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


# 注册扩展（扩展初始化）
def register_extensions(app):
    # p229 大部分扩展提供一个init_app()方法支持分离扩展的实例化和初始化操作
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)


# 注册蓝本
def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 注册自定义shell命令
def register_commands(app):
    # flask drop
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    # flask init 初始化创建管理员帐号
    # prompt为True，如果用户没有输入选择值，会提示形式请求输入；hide_input为True，会隐藏输入内容
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building BreakBlog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:  # 如果数据库中已有管理员记录就更新用户名和密码
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:  # 否则创建新的管理员记录
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='BreakBlog',
                blog_sub_title="You still have lots more to work on!",
                name='tw.huang',
                about='Hello World!.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    # flask forge 命令默认生成10个分类、50篇文章、500条评论
    # flask forge --category=20 --post=100 --comment=1000 命令生成20个分类、100篇文章、1000条评论
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from breakblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links
        # p240 更全面地生成虚拟数据，先删除再重建数据库表
        db.drop_all()
        db.create_all()
        # p240 生成虚拟数据顺序必须是 管理员-分类-文章-评论，links随意
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d categories...' % category)
        fake_categories(category)
        click.echo('Generating %d posts...' % post)
        fake_posts(post)
        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)
        click.echo('Generating links...')
        fake_links()
        click.echo('Done.')


# 注册错误处理函数
def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # P282 自定义CSRF错误响应
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


# 注册shell上下文处理函数
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


# 注册模板上下文处理函数
# p242 在基模板的导航栏和博客主页中需要使用博客的标题、副标题等，引入模板上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        # p284 管理员登录后，查询待审核评论的数量
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(
                reviewed=False).count()  # unread_comments 储存待审核评论的数量
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)
# 注册请求上下文处理函数


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['BREAKBLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response
