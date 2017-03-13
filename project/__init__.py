from flask import Flask, Response

app = Flask(__name__)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

from flask import Flask, render_template, request, redirect, url_for
import models, posts
from user import User


@app.route('/')
def index():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # add new user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # succesful creation
        if models.insertUser(username, password):
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
    # compare login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # succesful authentication
        if models.authenticateUser(username, password):
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
    redirect(url_from('login'))

@app.route('/blog')
def blog():
    if request.method == 'POST':
        if request.form == 'usrModify':
            # modify post
            return False
        elif request.form == 'usrPost':
            # add new post
            return False
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
