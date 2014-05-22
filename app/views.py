from app import app, db
from flask import render_template, flash, url_for, redirect, session
from forms import LoginForm, PostForm
from models import User, Post

@app.route('/index')
@app.route('/')
def index():
	posts = Post.query.all()
	return render_template("index.html", posts=posts)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'logged_in' in session:
		return render_template('admin.html')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
		if user:
			session['username'] = user.username
			session['user_id'] = user.id
			session['logged_in'] = True
			return redirect(url_for('post'))
		else:
			flash('Sorry, you are not registered.  Please contact the site owner to register.')
			return render_template('admin.html', form=form)
	return render_template('admin.html', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('username', None)
	flash('You were logged out')
	return redirect(url_for('index'))
	
@app.route('/post', methods=['GET', 'POST'])
def post():
	if 'logged_in' not in session:
		return redirect(url_for('admin'))
	form = PostForm()
	user_id = session['user_id'] 
	if form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, user_id=user_id)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live.')
		return redirect('index')
	return render_template('post.html', form=form)
	
@app.route('/delete/<int:id>')
def delete(id):
	if 'logged_in' not in session:
		return redirect(url_for('index'))
	post = Post.query.get(id)
	if post == None:
		flash('Post not found.')
		return redirect(url_for('index'))
	if post.user_id != session['user_id']:
		flash('You do not have rights to delete this post.')
		return redirect(url_for('index'))
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted.')
	return redirect(url_for('index'))

	