from app import app
from flask import render_template, url_for
from forms import AdminRegistrationForm

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
	form = AdminRegistrationForm()
	return render_template('admin.html', form=form)
