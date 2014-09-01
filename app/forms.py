from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, TextAreaField, validators

#Represents a form for logging in
class LoginForm(Form):
	username = TextField('username', [validators.InputRequired(), validators.Length(min=4, max=15)])
	password = TextField('password', [validators.InputRequired(), validators.Length(min=8, max=15)])

#Represents a form for creating blog posts	
class PostForm(Form):
	title = TextField('title', [validators.InputRequired(), validators.Length(min=1, max=140)])
	body = TextAreaField('body', [validators.InputRequired(), validators.Length(min=1, max=5000)])
	image_url = TextField('image_url', [validators.Length(max=500)])

	