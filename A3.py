from flask import Flask as f, render_template as r
from flask_bootstrap import Bootstrap as b

app = f(__name__)
bootstrap = b(app)
@app.route('/')
def index():
    return r('index.html')

@app.route('/user/<name>')
def user(name):
    return r('user.html', name=name)

bootstrap = b(app)