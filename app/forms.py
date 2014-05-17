from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, validators

class LoginForm(Form):
	user_name = TextField('username', [validators.Length(min=4, max=15)])
	password = TextField('password', [validators.Length(min=8, max=16)])

class AdminRegistrationForm(Form):
	first_name = TextField('first', [validators.InputRequired()]) 
	last_name = TextField('last', [validators.InputRequired()])
	user_name = TextField('username', [validators.Length(min=4, max=15)])
	password = TextField('password', [validators.Length(min=8, max=16)])