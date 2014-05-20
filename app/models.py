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
	posts = db.relationship('Post', backref='user', lazy='dynamic')

	def __init__(self, username, password, role=ROLE_USER):
		self.username = username
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User %r>' % (self.username)
		
class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	body = db.Column(db.String(5000))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	
	def __init__(self, title, body, user_id):
		self.title = title
		self.body = body
		self.user_id = user_id
	
	def __repr__(self):
		return '<Post %r>' % (self.title)

