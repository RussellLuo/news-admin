#!/usr/bin/env python
# -*- coding: utf-8 -*-

from news_admin.core import db
from . import hasher


user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(100), nullable=False, unique=True, index=True)
    password = db.Column(db.Unicode(100), nullable=False)
    email = db.Column(db.Unicode(100), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    roles = db.relationship('Role', secondary=user_role,
                            backref=db.backref('users', lazy='dynamic'))

    # ## Flask-Login integration
    # begin
    def is_authenticated(self):
        return self.is_staff

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    # end

    def set_password(self, password):
        self.password = hasher.make_password(password)

    def check_password(self, password):
        return hasher.check_password(password, self.password)

    def __repr__(self):
        return self.username


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(45))

    permissions = db.relationship('Permission', secondary=role_permission,
                                  backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return self.name


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(45), unique=True)
    description = db.Column(db.Unicode(100))

    def __repr__(self):
        return self.description or self.name
