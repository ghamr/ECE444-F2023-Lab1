from flask import Flask as f, render_template as r, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap as b
from flask_moment import Moment as m
from datetime import datetime as dt
from flask_wtf import FlaskForm as flaskform
from wtforms import SearchField as stringfield, SubmitField as submitfield
from wtforms.validators import DataRequired as datarequired

app = f(__name__)
bootstrap = b(app)
moment = m(app)
app.config['SECRET_KEY'] = 'hard to guess string'


class nameform(flaskform):
    name = stringfield('What is your name?', validators=[datarequired()])
    submit = submitfield('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = nameform()
    #comments from ch.4
    #this validate_on_submit thing checks that all the forms have been filled and only then returns true
    if form.validate_on_submit():
        #comments from ch.4
        #note: this session ['name'] thing is storing the name entered in the form in the cookies 
        ##this allows us to remember data between requests
        ##in this case, this is used to create a post/redirect/get pattern such that the server does not receive another post request 
        ###which would submit a duplicate form and is generally responsible for weird unwanted behaviour. 
        #note: should almost always redirect post requests
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you have changed your name!')
        session['name'] = form.name.data
        #the above replaces name = form.name.data
        form.name.date = ''
        return redirect(url_for('index'))
        #comments from ch.4
        #because we now have the name variable stored in the session,
        #that is what we need to return in case there are no new submit request (validate_on_submit fails)
    return r('index.html', form=form, name=session.get('name'), current_time=dt.utcnow())

@app.route('/user/<name>')
def user(name):
    return r('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return r('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return r('500.html'), 500
