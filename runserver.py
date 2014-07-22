#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from news_admin.core import app, db, admin
from news_admin import modules

if app.config.get('LOGGER_ENABLED'):
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOGGER_LEVEL', 'DEBUG')),
        format=app.config.get(
            'LOGGER_FORMAT',
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
        datefmt=app.config.get('LOGGER_DATE_FORMAT', '%d.%m %H:%M:%S')
    )

# 1. register all admins, import all models
modules.init(app)

# 2. create all tables
db.create_all()

# 3. save all permissions
admin.sync_perms()


app.run(debug=True)
