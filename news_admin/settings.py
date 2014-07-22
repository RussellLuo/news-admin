#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create MySQL database
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@server/db'
# app.config['SQLALCHEMY_ECHO'] = True

# Default password of admin user
USER_DEFAULT_PASSWORD = '123456'


# configure the logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'
