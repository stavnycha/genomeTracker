# all imports
from flask import Flask, url_for, flash, render_template, request, abort, redirect, session, g

# configuration
DATABASE = './genomeTracker/db/genometracker.db'
UPLOAD_FOLDER = 'genomeTracker/uploads/'
ALLOWED_EXTENSIONS = set(['txt'])
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GenomeTracker_SETTINGS', silent=True)
app.debug = DEBUG

from genomeTracker.db import *
from genomeTracker.utils import *
		   
@app.route('/')
def index():
	isLoggedIn = False
	try:
		isLoggedIn = session['username'] != None
		return render_template('welcome.html', isLoggedIn=isLoggedIn, username=session['username'])
	except KeyError:
		return render_template('welcome.html', isLoggedIn=False, username=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.method == 'POST':
		if request.form['password'] != request.form['password2']:
			error = 'Passwords do not match'
		else:
			user = getUser(request.form['username'], None)
			if (user == None):
				add_user(request.form['username'], request.form['email'], request.form['password'])
				flash('New user was successfully added')
				session['username'] = request.form['username']
				return redirect(url_for('upload'))
			else:
				error = 'User with this name already exists'
	return render_template('signup.html', error=error, username=None)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		user = getUser(request.form['username'], request.form['password'])
		if user == None:
			error = 'Invalid credentials'
		else:
			flash('You were successfully logged in')
			session['username'] = request.form['username']
			return redirect(url_for('upload'))
	return render_template('login.html', error=error, username=None)
		
@app.route('/upload')
def upload():
	try:
		return render_template('upload.html', username=session["username"])
	except KeyError:
		abort(403)

@app.route('/report', methods=['POST'])
def report():
	try:
		report = processFile(request.files['file'])
		return render_template('report.html', report=report, username=session["username"])
	except ExtensionNotAllowedException:
		return redirect(url_for('upload', error='Extension is not allowed'))
	except KeyError:
		abort(403)
		
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403
	
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

import subprocess

@app.route ( "/repo_push" )
def repo_push ():
    subprocess.call ( ["bash", "/home/www/pull_repo.sh"] )
    return redirect(url_for('index'))
	
if __name__ == '__main__':
    app.run()