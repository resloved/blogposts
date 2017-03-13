import sqlite3 as sql

q = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    user TEXT NOT NULL,
    body TEXT NOT NULL
);
"""

con = sql.connect("posts.db")
cur = con.cursor()
cur.execute(q)

def newPost(title, user, body):
    con = sql.connect("posts.db")
    cur = con.cursor()
    cur.execute("INSERT INTO posts (title, user, body) VALUES (?,?,?)",
                (title, user, body))
    con.commit()
    con.close()


def modifyPost(id, title, user, body):
    con = sql.connect("posts.db")
    cur = con.cursor()
    cur.execute("REPLACE INTO posts (id, title user, body) VALUES (?,?,?,?)",
            (id, title, user, body))
    con.commit()
    con.close()


def getPosts():
    con = sql.connect("posts.db")
    cur = con.cursor()
    cur.execute("SELECT id, title, user, body FROM posts")
    data = cur.fetchall()
    con.close()
    posts = []
    for tuple in data:
        posts.append(Post(tuple[0], tuple[1], tuple[2], tuple[3]))
    return posts


class Post:
    def __init__(self, id, title, user, body):
        self.id = id
        self.title = title
        self.user = user
        self.body = body
