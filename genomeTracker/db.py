import sqlite3
from flask import g
from contextlib import closing
from genomeTracker import app

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
	
@app.before_request
def before_request():
	g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
	
def add_user(username, email, password):
    g.db.execute('insert into users (username, email, password) values (?, ?, ?)',
                 [username, email, password])
    g.db.commit()
	
def getUser(username, password):
	if (password != None):
		return query_db('select * from users where username = ? and password = ?', [username, password], one=True)
	else:
		return query_db('select * from users where username = ?', [username], one=True)