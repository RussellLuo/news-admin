#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from wtforms import PasswordField

from news_admin.core import app, admin, ModelView
from .models import User, Role, Permission

NOW = datetime.datetime.now


class UserAdmin(ModelView):
    relative_permission = 'user'

    column_list = ('username', 'email', 'is_superuser',
                   'date_joined', 'last_login')
    column_labels = dict(
        username=u'用户名',
        email=u'邮箱',
        is_superuser=u'是否管理员',
        date_joined=u'注册时间',
        last_login=u'最后登录时间',
        roles=u'角色分配',
    )
    column_exclude_list = ('password',)
    column_searchable_list = ('username',)

    form_excluded_columns = ('password', 'last_login')
    form_columns = ('username', 'email', 'is_superuser', 'roles')

    # `password` field is processed sepcially
    # by overriding `scaffold_form()` and `on_model_change()` methods
    #
    # This solution is from https://github.com/mrjoes/flask-admin/issues/173

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField(u'密码')
        return form_class

    def on_model_change(self, form, model):
        # set some defaults
        if model.date_joined is None:
            model.date_joined = NOW()

        if model.is_staff is None:
            model.is_staff = True

        if len(model.password2):
            model.set_password(form.password2.data)
        else:
            if model.password is None:
                model.set_password(app.config['USER_DEFAULT_PASSWORD'])


class RoleAdmin(ModelView):
    relative_permission = 'role'

    column_list = ('name', 'permissions')
    column_labels = dict(name=u'名称', permissions=u'权限分配')

    form_columns = ('name', 'permissions')


class PermissionAdmin(ModelView):
    can_create = False
    can_delete = False

    column_list = ('name', 'description')
    column_labels = dict(name=u'名称', description=u'描述')

    form_excluded_columns = ('name', 'roles')


admin.register(User, UserAdmin, name=u'用户', category=u'用户管理')
admin.register(Role, RoleAdmin, name=u'角色', category=u'用户管理')
admin.register(Permission, PermissionAdmin, name=u'权限', category=u'用户管理')
