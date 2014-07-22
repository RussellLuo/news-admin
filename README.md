news-admin
==========

An administration backend for news based on Flask-Admin.


1. Configure database
---------------------

1) create database

    $ mysql -uroot -p
    mysql> CREATE DATABASE news;

2) change settings

    $ cd news_admin
    $ vi settings.py
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/news'

2. Run it
---------

    $ cd news-admin
    $ virtualenv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ easy_install flask-htmlbuilder
    (env)$ python runserver.py
