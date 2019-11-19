# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, URL, Email

from breakblog.models import Category


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


# 文章表单
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 30)])
    # 自定义文章副标题
    subtitle = TextAreaField('Subtitle', validators=[
                             DataRequired(), Length(1, 255)])
    # p247 SelectField字段由WTForms提供
    category = SelectField('Category', coerce=int, default=1)
    # CKEditorField字段由flask-ckeditor提供
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # p247 choices必须是一个包含两元素元组的列表，列表中的元组分别包含选项值和选项标签
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]


# 分类表单
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        # p248 查询数据库Category表单中是否存在同名记录，如果是的话就抛出ValidationError异常
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


# 评论表单
class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(1, 254)])
    # p248 Optional验证器可使字段为空，URL验证器确保输入数据为有效的URL
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


# 管理器的评论表单
class AdminCommentForm(CommentForm):
    # p249 HiddenField类代表隐藏字段，即html中的<input type="hidden">
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


# Links表单
class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[
                      DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()


# 设置表单
class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[
                             DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[
                                 DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()
