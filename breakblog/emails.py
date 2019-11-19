# -*- coding: utf-8 -*-
"""
    :author: tw.huang
    :github_url: https://github.com/tw-huang
    :email: tw.huang@foxmail.com
"""
from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from breakblog.extensions import mail


# p191 使用异步发送电子邮件
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


# p251 send_new_comment_email() 文章被游客回复提醒邮件
def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id,
                       _external=True) + '#comments'
    send_mail(subject='New comment', to=current_app.config['BREAKBLOG_EMAIL'],
              html='<p>New comment in post <i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (post.title, post_url, post_url))


# p251 send_new_reply_email() 发送新回复提醒邮件给游客
def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id,
                       _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (comment.post.title, post_url, post_url))
