from flask import Flask, Response

app = Flask(__name__)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

from flask import Flask
from flask import render_template
from flask import request
import models


@app.route("/")
def index():
    return Response("Hello World!"), 200


@app.route('/signup', methods=['POST', 'GET'])
def home():
    users = models.retrieveUsers()
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        models.insertUser(username, password)
        return render_template('index.html', users=users)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
