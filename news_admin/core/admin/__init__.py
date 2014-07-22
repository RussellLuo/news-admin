#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.ext.admin
from ..app import app
from ..db import db


class Admin(flask.ext.admin.Admin):

    permissions = set()

    def register(self, model, view, *args, **kwargs):
        self.add_view(view(model, db.session, *args, **kwargs))

        # collect possible permissions
        rel_perm = getattr(view, 'relative_permission', None)
        if rel_perm:
            self.permissions.add(rel_perm)

    def sync_perms(self):
        """Save all relative permissions into database."""
        from ...modules.accounts.models import Permission
        for rel_perm in self.permissions:
            if not db.session.query(Permission).filter_by(name=rel_perm).first():
                perm = Permission()
                perm.name = rel_perm
                db.session.add(perm)
                db.session.commit()


def create_admin():
    from .views import AdminIndexView
    return Admin(app, u'新闻后台',
                 index_view=AdminIndexView(template='index.html'),
                 base_template='base.html')


admin = create_admin()
