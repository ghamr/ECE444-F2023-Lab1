from flask import Flask as f
app = f(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
