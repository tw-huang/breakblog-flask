# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()  # 富文本编辑器即WYSIWYG（What You See Is What You Get）
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()


# p276 获取当前用户
@login_manager.user_loader  # @login_manager.user_loader装饰器，接收用户id为参数，返回对应的用户对象
def load_user(user_id):
    from breakblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


# p280 视图保护
login_manager.login_view = 'auth.login'

login_manager.login_message_category = 'warning'

# 可进行自定义提示消息
# login_manager.login_message = '请先登录再进行操作！'
