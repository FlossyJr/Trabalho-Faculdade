import os
import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.sqlite')


class User(UserMixin):
def __init__(self, id, username, password_hash):
self.id = str(id)
self.username = username
self.password_hash = password_hash


@staticmethod
def get_by_username(username):
db = get_db()
cur = db.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
row = cur.fetchone()
if not row:
return None
return User(row[0], row[1], row[2])


@staticmethod
def get_by_id(id):
db = get_db()
cur = db.execute('SELECT id, username, password_hash FROM users WHERE id = ?', (id,))
row = cur.fetchone()
if not row:
return None
return User(row[0], row[1], row[2])


def check_password(self, password):
return check_password_hash(self.password_hash, password)




def get_db():
db = getattr(g, '_database', None)
if db is None:
db = g._database = sqlite3.connect(DATABASE_PATH)
db.row_factory = sqlite3.Row
return db




def init_db(app=None):
if app is None:
from flask import current_app as app
with app.app_context():
db = get_db()
cur = db.cursor()
# create tables if not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password_hash TEXT NOT NULL
)
''' )
db.commit()


# ensure admin exists from env
from os import getenv
admin_user = getenv('ADMIN_USER')
admin_pass = getenv('ADMIN_PASS')
if admin_user and admin_pass:
cur = db.execute('SELECT id FROM users WHERE username = ?', (admin_user,))
if not cur.fetchone():
hashed = generate_password_hash(admin_pass)
db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (admin_user, hashed))
db.commit()