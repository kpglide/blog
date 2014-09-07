from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, TextAreaField, validators
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField

#Represents a form for logging in
class LoginForm(Form):
	username = TextField('username', [validators.InputRequired(), validators.Length(min=4, max=15)])
	password = TextField('password', [validators.InputRequired(), validators.Length(min=8, max=15)])

#Represents a form for creating blog posts	
class PostForm(Form):
	title = TextField('title', [validators.InputRequired(), validators.Length(min=1, max=140)])
	body = PageDownField('body', [validators.InputRequired()])
	image1_url = TextField('image1_url', [validators.Length(max=500)])
	image2_url = TextField('image2_url', [validators.Length(max=500)])
	image3_url = TextField('image3_url', [validators.Length(max=500)])

	