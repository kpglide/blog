from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
					validators, ValidationError

#Represents a form for logging in
class LoginForm(Form):
	username = TextField('username', [validators.InputRequired()])
	password = PasswordField('password', [validators.InputRequired()])
	remember_me = BooleanField('Keep me logged in')

	