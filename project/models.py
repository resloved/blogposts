import sqlite3 as sql

q = ""

con = sql.connect("database.db")
cur = con.cursor()
cur.execute(q)

# From: https://gist.github.com/PolBaladas/07bfcdefb5c1c57cdeb5

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users
