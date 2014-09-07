from . import db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from markdown import markdown
import bleach

ROLE_USER = 0
ROLE_ADMIN = 1

#Represents individual blog users, each with an associated username, password
#role and various blog posts.
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

#Represents blog posts, each having a title, body and timestamp, plus
#an association with an individual user		
class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	image1_url = db.Column(db.String(500), nullable=True)
	image2_url = db.Column(db.String(500), nullable=True)
	image3_url = db.Column(db.String(500), nullable=True)
	body_html = db.Column(db.Text)

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
						'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
						'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format="html"),
			tags=allowed_tags, strip=True))

	def __init__(self, title, body, user_id, image1_url, image2_url, image3_url,
				 timestamp=None):
		self.title = title
		self.body = body
		self.user_id = user_id
		if timestamp is None:
			timestamp = datetime.utcnow()
		self.timestamp = timestamp
		self.image1_url = image1_url
		self.image2_url = image2_url
		self.image3_url = image3_url
	
	def __repr__(self):
		return '<Post %r>' % (self.title)

db.event.listen(Post.body, 'set', Post.on_changed_body)