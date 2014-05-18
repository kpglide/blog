from app import app
from flask import render_template, url_for, redirect
from forms import LoginForm

@app.route('/index')
@app.route('/')
def index():
	#This is dummy data used for testing
	user = {'nickname': 'kevin'}
	posts = [
		{
			'author': {'nickname': 'kevin'},
			'body': 'Great day in Atl'
		},
		{	'author': {'nickname': 'Gibson'},
			'body': "I'm hungry"
		},
		{	'author': {'nickname': 'Gouda'},
			'body': "I got a haircut"
		}
	]
	return render_template("index.html", user=user, posts=posts)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		return redirect('/index')
	return render_template('admin.html', form=login_form)
