from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, validators

class LoginForm(Form):
	username = TextField('username', [validators.InputRequired(), validators.Length(min=4, max=15)])
	password = TextField('password', [validators.InputRequired(), validators.Length(min=8, max=16)])