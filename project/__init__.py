from flask import Flask, Response

app = Flask(__name__)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

from flask import Flask, render_template, request, redirect, url_for, session
import models, posts, os
from user import User
from wtforms import Form, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

@app.route('/')
def index():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm(request.form)
    # add new user
    if request.method == 'POST' and form.validate():
        # succesful creation
        if models.insertUser(form.username.data, form.password.data):
            users = models.retrieveUsers()
            return render_template \
                ('index.html', users=users)
        # failed creation
        else:
            users = models.retrieveUsers()
            return render_template \
                ('index.html', users=users, error='Name Taken')
    # main
    users = models.retrieveUsers()
    return render_template('index.html', users=users)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = RegistrationForm(request.form)
    # compare login
    if request.method == 'POST' and form.validate():
        # succesful authentication
        if models.authenticateUser(form.username.data, form.password.data):
            session['user'] = username
            return redirect(url_for('blog'))
        # failed authentication
        else:
            error = "Incorrect username or password"
            return render_template('login.html', error=error)
    # main
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        # modify post
        if 'usrModify' in request.form:
            return False
        # new post
        elif 'usrPost' in request.form:
            title = request.form['title']
            body = request.form['body']
            posts.newPost(title, session['user'], body)
        blog = posts.getPosts()
        # TODO: find better method
        if 'user' in session:
            return render_template \
                ('blog.html', blog=blog, authorized=session['user'])
        return render_template('blog.html', blog=blog)
    else:
        blog = posts.getPosts()
        if 'user' in session:
            return render_template \
                ('blog.html', blog=blog, authorized=session['user'])
        return render_template('blog.html', blog=blog)

app.secret_key = os.urandom(24)
