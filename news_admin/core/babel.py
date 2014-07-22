#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, session
from flask.ext.babelex import Babel

babel = Babel()


def init(app):
    babel.init_app(app)


@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')
