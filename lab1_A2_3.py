from flask import Flask as f
app = f(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

##A2_4
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

    