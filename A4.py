from flask import Flask as f, render_template as r, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap as b
from flask_moment import Moment as m
from datetime import datetime as dt
from flask_wtf import FlaskForm as flaskform
from wtforms import SearchField as stringfield, SubmitField as submitfield, ValidationError
from wtforms.validators import DataRequired as datarequired, Email as mail, Regexp as regexp

app = f(__name__)
bootstrap = b(app)
moment = m(app)
app.config['SECRET_KEY'] = 'hard to guess string'


#this is the way you would define a custom validator
#this was created by imitating this stack overflow post:
# https://stackoverflow.com/questions/50327174/custom-validators-in-wtforms-using-flask
def at_validator(form, field):
       if '@' not in field.data:
            raise ValidationError(f"Please include an \'@\' in the email address \'{field.data}\' is missing an \'@\'")

class nameform(flaskform):
    
    name = stringfield('What is your name?', validators=[datarequired(message='fill this field please and thank you')])
    email = stringfield('What is your UofT Email address?', validators=[datarequired(), mail(), at_validator])
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
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
            
        session['name'] = form.name.data
        session['email'] = form.email.data
        #the above replaces name = form.name.data
        return redirect(url_for('index'))
        #comments from ch.4
        #because we now have the name variable stored in the session,
        #that is what we need to return in case there are no new submit request (validate_on_submit fails)
    return r('index.html', form=form, name=session.get('name'), current_time=dt.utcnow(), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return r('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return r('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return r('500.html'), 500
