# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from breakblog.forms import LoginForm
from breakblog.models import Admin
from breakblog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)

# p277 登入用户
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # p278 避免已经登录的用户不小心访问这个视图，如果是，重定向到首页
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
