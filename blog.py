from flask import Flask, render_template, request, session, redirect, url_for, flash, g
import sqlite3
from functools import wraps

DATABASE = "blog.db"
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != app.config['PASSWORD'] or \
            request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Credential, Please try again!'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not post or not title:
        flash("All fields are required, Please try again!")
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts (title, post) VALUES (?, ?)', [title, post])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted.')
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)