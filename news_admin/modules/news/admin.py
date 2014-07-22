#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import fields, widgets

from news_admin.core import admin, ModelView, adjust_priority
from .models import (
    News, Channel,
    ScrollableNews, HeadlineNews,
)


# Define wtforms widget and field
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class NewsAdmin(ModelView):
    relative_permission = 'news'

    column_list = ('title', 'sub_title', 'publish_time',
                   'fake_pv', 'actual_pv')
    column_labels = dict(
        title=u'标题',
        sub_title=u'副标题',
        thumb_url=u'缩略图',
        content=u'正文',
        source=u'来源',
        publish_time=u'发布时间',
        fake_pv=u'浏览次数',
        actual_pv=u'实际浏览次数',
        author=u'作者',
        channel=u'栏目',
    )
    column_searchable_list = ('title',)
    page_size = 10

    form_overrides = dict(content=CKTextAreaField)


class ChannelAdmin(ModelView):
    relative_permission = 'channel'

    column_list = ('name', 'description')
    column_labels = dict(name=u'名称', description=u'描述')


class ScrollableNewsAdmin(ModelView):
    relative_permission = 'scrollable_news'

    column_list = ('news', 'adjust_priority')
    column_labels = dict(news=u'新闻', priority=u'显示顺序',
                         image_url=u'图片', adjust_priority=u'调整顺序')
    column_default_sort = 'priority'
    column_formatters = {
        'adjust_priority': adjust_priority
    }

    form_excluded_columns = ('priority',)


class HeadlineNewsAdmin(ModelView):
    relative_permission = 'headline_news'

    column_list = ('news',)
    column_labels = dict(news=u'新闻', channel=u'栏目', image_url=u'图片')


admin.register(News, NewsAdmin, name=u'新闻', category=u'新闻管理')
admin.register(Channel, ChannelAdmin, name=u'栏目', category=u'新闻管理')
admin.register(ScrollableNews, ScrollableNewsAdmin,
               name=u'滚动新闻', category=u'滚动热点头条视频')
admin.register(HeadlineNews, HeadlineNewsAdmin,
               name=u'头条新闻', category=u'滚动热点头条视频')
