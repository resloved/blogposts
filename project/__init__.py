from flask import Flask, Response

app = Flask(__name__)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

from flask import Flask, render_template, request
import models


@app.route('/')
def index():
    return Response("Hello World!"), 200


@app.route('/signup', methods=['POST', 'GET'])
def home():
    # add new user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        models.insertUser(username, password)
        return render_template('index.html')
    else:
        users = models.retrieveUsers()
        return render_template('index.html', users=users)


@app.route('/login', methods=['POST', 'GET'])
def authenticate():
    # compare login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if models.authenticateUser(username, password):
            return render_template('authenticated.html')
        else:
            # error messaage
            error = "Incorrect username or password"
            return render_template('login.html', error)
    else:
        return render_template('login.html')
