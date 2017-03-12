import sqlite3 as sql

q = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
"""

con = sql.connect("database.db")
cur = con.cursor()
cur.execute(q)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

# Returns True if succesfully added
def insertUser(username, password):
    if getUser(username) is not None:
        return False
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)",
                (username, password))
    con.commit()
    con.close()
    return True


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users


def getUser(username):
    user = None
    users = retrieveUsers()
    for user in users:
        if user[0] is username:
            return user
    return user


def authenticateUser(name, password):
    user = getUser(name)
    if user is not None:
        # compare password
        return password is user[1]
    return False
