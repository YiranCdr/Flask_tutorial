# coding:utf8
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据。
    # 把连接储存于其中，可以多次使用，而不用在同一个 请求中每次调用 get_db 时都创建一个新的连接。
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES,
        )
        # sqlite3.Row 告诉连接返回类似于字典的行，这样可以通过列名称来操作 数据。
        g.db.row_factory = sqlite3.Row
    return g


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    # 每个请求处理函数中可以通过 get_db() 来得到当前打开的数据库连接。
    db = get_db()
    with current_app.open_resources('schema.sql') as f:
        db.excutescript(f.read().decode('utf8'))


# Click 是用 Python 写的一个第三方模块，用于快速创建命令行。
# 使用 @click.command() 装饰一个函数，使之成为命令行接口
# 使用 @click.option() 等装饰函数，为其添加命令行选项等。
@click.command('init-db')
# Commands added using the Flask app’s cli command() decorator will be executed
# with an application context pushed,
# so your command and extensions have access to the app and its configuration.
# If you create a command using the Click command() decorator instead of the Flask decorator,
# you can use with_appcontext() to get the same behavior.
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialized. ')
