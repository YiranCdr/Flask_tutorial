# coding:utf8
import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    print app.instance_path
    if test_config is None:
        app.config.from_pyfile('settings.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        # 如果要创建的目录已经存在，那么makedir会报错。
        os.makedirs(app.instance_path)
    except Exception:
        pass

    @app.route('/hello')
    def hello():
        return 'hello world!'

    # register
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.blue_print)


    return app


