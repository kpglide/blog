from app import db
from flask.ext.sqlalchemy import SQLAlchemy

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True)
	password = db.Column(db.String(25), unique=True)
	role = db.Column(db.SmallInteger, default=ROLE_USER)

	def __init__(self, username, password, role=ROLE_USER):
		self.username = username
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User %r>' % (self.username)

