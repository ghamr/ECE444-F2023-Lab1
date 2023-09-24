from flask import Flask as f, render_template as r
from flask_bootstrap import Bootstrap as b
from flask_moment import Moment as m
from datetime import datetime as dt

app = f(__name__)
bootstrap = b(app)
moment = m(app)


@app.route('/')
def index():
    return r('index.html', current_time=dt.utcnow())

@app.route('/user/<name>')
def user(name):
    return r('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return r('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return r('500.html'), 500
