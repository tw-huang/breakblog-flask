# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
import random

from faker import Faker

from sqlalchemy.exc import IntegrityError

from breakblog.models import Admin, Category, Post, Comment, Link
from breakblog.extensions import db

fake = Faker('zh_CN')  # Faker('zh_CN') 创建中文虚拟数据


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='BreakBlog',
        blog_sub_title='You still have lots more to work on!',
        name='tw.huang',
        about='Hello World!'
    )
    admin.set_password('helloworld')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    # p237 先创建默认分类Default，然后依次生成随机名称的虚拟分类
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        # p237 因为分类名称不能重复，所以try except捕捉异常
        try:
            db.session.commit()
        except IntegrityError:  # 出现sqlalchemy.exc.IntegrityError异常
            db.session.rollback()  # 回滚操作


def fake_posts(count=50):
    # p238 默认生成50篇文章
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            subtitle=fake.text(random.randint(30, 255)),  # 文章副标题字数为（60-255）随机数
            body=fake.text(2000),
            # p238 每篇文章指定一个随机分类，get()方法获取，传入主键值为1到所有文章分类数量数字之间的随机值
            category=Category.query.get(
                random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    # 默认生成500条评论
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # 默认生成50条：未审核评论、管理员评论、回复
    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核的评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员发表的评论
        comment = Comment(
            author='tw.huang',
            email='tw.huang@foxmail.com',
            site='http://www.breakblog.me',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(
                random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
