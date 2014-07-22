#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask


def create_app():
    app = Flask('news_admin')
    app.config.from_object('news_admin.settings')

    from . import babel
    babel.init(app)

    return app


app = create_app()
