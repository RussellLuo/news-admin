#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext import login
from flask.ext.admin.contrib import sqla
from flask.ext.htmlbuilder import html


def adjust_priority(view, context, model, name):
    _href = '/admin/adjust-priority?url=%s&model=%s&id=%s' % (
        view.url, model.__class__.__name__, model.id
    )
    _i = lambda icon: html.i(class_="icon %s" % icon, style="margin-right: 5px;")()
    return html.div()(
        html.a(href=_href + '&delta=-1')(_i('icon-circle-arrow-up')),
        html.a(href=_href + '&delta=1')(_i('icon-circle-arrow-down')),
    )


# Customized admin interface
class ModelView(sqla.ModelView):
    relative_permission = None

    create_template = 'create.html'
    edit_template = 'edit.html'

    def is_accessible(self):
        user = login.current_user
        if user.is_authenticated():
            # superuser has all permissions
            if user.is_superuser:
                return True
            # check permissions of normal user
            for role in user.roles:
                permissions = [perm.name for perm in role.permissions]
                if self.relative_permission in permissions:
                    return True
        return False
