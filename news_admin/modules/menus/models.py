#!/usr/bin/env python
# -*- coding: utf-8 -*-

from news_admin.core import db


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(100), nullable=False, index=True)
    url = db.Column(db.Unicode(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'))

    sub_menus = db.relationship('Menu')

    def __repr__(self):
        return self.title
