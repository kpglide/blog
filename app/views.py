from app import app, db
from flask import render_template, flash, url_for, redirect, session, request,\
					Response
from forms import LoginForm, PostForm
from models import User, Post
from config import POSTS_PER_PAGE
import time, os, json, base64, hmac, urllib
from hashlib import sha1

#Display home page showing a paginated list of blog posts
@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('index.html', posts=posts)

#Display admin page where registered users are able to login
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

#Display post page where a logged in user may draft and submit a blog post	
@app.route('/post', methods=['GET', 'POST'])
def post():
	if 'logged_in' not in session:
		return redirect(url_for('admin'))
	form = PostForm()
	user_id = session['user_id'] 
	if form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, user_id=user_id, 
					image_url=form.image_url.data)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live.')
		return redirect('index')
	return render_template('post.html', form=form)

@app.route('/sign_s3/')
def sign_s3():
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    object_name = request.args.get('s3_object_name')
    mime_type = request.args.get('s3_object_type')

    expires = long(time.time()+10)
    amz_headers = "x-amz-acl:public-read"

    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
    signature = urllib.quote_plus(signature.strip())

    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
         'url': url
      })

    return Response(content, mimetype='text/plain; charset=x-user-defined')
	
#Delete a blog post
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

#Display the web app's about page
@app.route('/about')
def about():
	return render_template('about.html')
	