#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import form, fields, validators

from ..db import db
from ...modules.accounts.models import User


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    username = fields.TextField(u'用户名', validators=[validators.required(u'请输入用户名')])
    password = fields.PasswordField(u'密码', validators=[validators.required(u'请输入密码')])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError(u'用户不存在')

        if not user.is_staff:
            raise validators.ValidationError(u'非后台用户')

        if not user.check_password(self.password.data):
            raise validators.ValidationError(u'密码错误')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()


class RegisterForm(form.Form):
    username = fields.TextField(u'用户名', validators=[validators.required(u'请输入用户名')])
    email = fields.TextField(u'邮箱', validators=[validators.required(u'请输入邮箱')])
    password = fields.PasswordField(u'密码', validators=[validators.required(u'请输入密码')])
    is_superuser = fields.HiddenField(default='')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError(u'用户名已存在')
