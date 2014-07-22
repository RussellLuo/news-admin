#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import importlib
import logging

logger = logging.getLogger(__name__)


def init(app):
    """Import `modules.module.admin`."""

    modules_path = 'modules'
    admin_name = 'admin'

    base_name = '.'.join([app.name, modules_path])
    path = os.path.dirname(__file__)
    dir_list = os.listdir(path)
    for fname in dir_list:
        if (os.path.isdir(os.path.join(path, fname)) and
            os.path.exists(os.path.join(path, fname, '__init__.py'))):

            # just import admin
            module_name = '.'.join([base_name, fname, admin_name])
            try:
                importlib.import_module(module_name)
            except ImportError:
                logger.warning('can\'t import "%s"' % module_name)
