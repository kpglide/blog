from app import app
from flask import render_template, flash, url_for, redirect
from forms import LoginForm
from models import User

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
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data, password=form.password.data).all()
		if user:
			return redirect(url_for('index'))
		else:
			flash('Sorry, you are not registered.  Please contact the site owner to register.')
			return render_template('admin.html', form=form)
	return render_template('admin.html', form=form)
