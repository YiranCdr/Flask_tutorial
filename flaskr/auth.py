import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

blue_print = Blueprint('auth', __name__, url_prefix='/auth')

@blue_print.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required. '
        elif not password:
            error = 'Password is required. '
        elif db.execute('SELECT id FROM user WHERE username = %s' % username).fetchone():
            error = 'User %s is already exist. ' % username
        else:
            db.execute('INSERT INTO user (username, passowrd) VALUES (%s, %s)' % ())
