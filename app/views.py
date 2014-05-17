from app import app
from flask import render_template, url_for

@app.route('/')
def index():
	user = {'nickname': 'kevin'}
	posts = [
		{
			'author': {'nickname': 'kevin'},
			'body': 'Great day in Atl'
		},
		{	'author': {'nickname': 'Gibson'},
			'body': "I'm hungry"
		}
	]
	return render_template("index.html", user=user, posts=posts)