from flask import Flask, Response

app = Flask(__name__)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

from flask import Flask, render_template, request
import models, posts
from user import User


current = False

@app.route('/')
def index():
    return Response("Hello World!"), 200


@app.route('/signup', methods=['POST', 'GET'])
def home():
    # add new user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if models.insertUser(username, password):
            return render_template('index.html', users=users)
        else:
            return render_template('index.html', error='Name Taken')
    else:
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
            current = User(username, True)
            return redirect(url_for('/blog'))
        # failed authentication
        else:
            error = "Incorrect username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    if current not None:
        current = None
        return redirect(url_for('/login'))

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
        if current is not None:
            return render_template \
                ('blog.html', blog=blog, authorized = current)
        return render_template('blog.html', blog=blog)
    else:
        blog = posts.getPosts()
        if current is not None:
            return render_template \
                ('blog.html', blog=blog, authorized = current)
        return render_template('blog.html', blog=blog)
