from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
					validators, ValidationError

#Represents a form for logging in
class LoginForm(Form):
	username = TextField('username', [validators.InputRequired(), validators.Length(min=4, max=15)])
	password = PasswordField('password', [validators.InputRequired(), validators.Length(min=8, max=15)])
	remember_me = BooleanField('Keep me logged in')

	