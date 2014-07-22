#!/usr/bin/env python
# -*- coding: utf-8 -*-

from news_admin.core import admin, ModelView
from .models import Menu


class MenuAdmin(ModelView):
    relative_permission = 'menu'

    column_list = ('title', 'url', 'sub_menus')
    column_labels = dict(title=u'名称', url=u'链接', sub_menus=u'子菜单')


admin.register(Menu, MenuAdmin, name=u'导航菜单')
