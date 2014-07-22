#!/usr/bin/env python
# -*- coding: utf-8 -*-

from news_admin.core import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(100), nullable=False)
    sub_title = db.Column(db.Unicode(100))
    thumb_url = db.Column(db.Unicode(100))
    content = db.Column(db.UnicodeText, nullable=False)
    source = db.Column(db.Unicode(100))
    publish_time = db.Column(db.DateTime(), nullable=False)
    fake_pv = db.Column(db.Integer, default=0)
    actual_pv = db.Column(db.Integer, default=0)
    author = db.Column(db.Unicode(100), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))

    channel = db.relationship('Channel')

    def __repr__(self):
        return self.title


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    description = db.Column(db.Unicode(100))

    def __repr__(self):
        return self.description or self.name


class ScrollableNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    image_url = db.Column(db.Unicode(100), nullable=False)
    priority = db.Column(db.Integer, default=0)

    news = db.relationship('News')

    def __repr__(self):
        return self.news.title


class HeadlineNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    image_url = db.Column(db.Unicode(100), nullable=False)

    channel = db.relationship('Channel')
    news = db.relationship('News')

    def __repr__(self):
        return self.news.title
