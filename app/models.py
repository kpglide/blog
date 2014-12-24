from . import db
from . import login_manager
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
from flask.ext.login import UserMixin

ROLE_USER = 0
ROLE_ADMIN = 1

#Represents individual blog users, each with an associated username, password
#role and various blog posts.
class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True)
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	posts = db.relationship('Post', backref='user', lazy='dynamic')
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __init__(self, username, password, role=ROLE_USER):
		self.username = username
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User %r>' % (self.username)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

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

	def __init__(self, title, body, user_id, image1_url=None, image2_url=None, image3_url=None,
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

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))