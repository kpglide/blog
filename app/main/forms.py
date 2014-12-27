from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, TextAreaField, validators
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField

#Represents a form for creating blog posts	
class PostForm(Form):
	title = TextField('title', [validators.InputRequired('*You must include a title*'), validators.Length(min=1, max=140)])
	body = PageDownField('body', [validators.InputRequired('*You must include a body*')])
	image1_url = TextField('image1_url', [validators.Length(max=500)])
	image2_url = TextField('image2_url', [validators.Length(max=500)])
	image3_url = TextField('image3_url', [validators.Length(max=500)])

	