#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from flask import url_for, redirect, request
from flask.ext import admin, login
from flask.ext.admin import helpers, expose

from ..app import app
from ..db import db
from .forms import LoginForm, RegisterForm
from ...modules.accounts.models import User

NOW = datetime.datetime.now


@app.route('/')
def index():
    return u'<a href="/admin/">点击进入新闻后台</a>'


@app.route('/admin/adjust-priority', methods=('GET',))
def adjust_priority():
    url = request.args.get('url', '/admin')
    _id = int(request.args.get('id'))
    delta = int(request.args.get('delta'))

    model_name = request.args.get('model')
    model_cls = db.Model._decl_class_registry.get(model_name)
    if model_cls:
        ids = [
            row.id
            for row in db.session.query(model_cls.id).order_by('priority').all()
        ]
        old_index = ids.index(_id)
        ids.remove(_id)
        new_index = old_index + delta
        if new_index < 0:
            new_index = 0
        ids.insert(new_index, _id)

        for i, v in enumerate(ids):
            model = db.session.query(model_cls).get(v)
            model.priority = i
            db.session.merge(model)
        db.session.commit()

    return redirect(url)


# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login'))
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            user.last_login = NOW()
            db.session.merge(user)
            db.session.commit()

            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))

        link = u'<p>还没有帐号？ <a href="%s">马上注册</a></p>' % url_for('.register')
        self._template_args['form'] = form
        self._template_args['link'] = link

        return super(AdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register(self):
        form = RegisterForm(request.form)

        # hacks to register a superuser
        if request.method == 'GET':
            form.is_superuser.data = request.args.get('is_superuser', '')

        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            user.set_password(form.password.data)
            user.is_staff = True
            user.is_superuser = bool(form.is_superuser.data)
            user.date_joined = NOW()

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))

        link = u'<p>已经有了帐号？ <a href="%s">马上登录</a></p>' % url_for('.login')
        self._template_args['form'] = form
        self._template_args['link'] = link

        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Initialize Flask-Login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

init_login()
