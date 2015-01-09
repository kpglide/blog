from .. import db
from flask import render_template, flash, url_for, redirect, session, request,\
					current_app, make_response, Response
from . import main
from .forms import PostForm
from ..models import User, Post
import time, os, json, base64, hmac, urllib
from hashlib import sha1
from flask.ext.login import login_required, current_user

#Display home page showing a paginated list of blog posts
@main.route('/')
@main.route('/index')
@main.route('/index/<int:page>')
def index(page=1, type=int):
	page = request.args.get('page', page, type)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, 
								per_page=current_app.config['POSTS_PER_PAGE'])
	posts = pagination.items
	return render_template('index.html', posts=posts, pagination=pagination)

#Display unique page for each post
@main.route('/single_post/<int:id>')
def single_post(id):
	entry = Post.query.get_or_404(id)
	return render_template('index.html', posts=[entry], single_post=True)

#Display post page where a logged in user may draft and submit a blog post	
@main.route('/post', methods=['GET', 'POST'])
@login_required
def post():
	form = PostForm()
	user_id = session['user_id'] 
	if form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, 
					user_id=user_id, image1_url=form.image1_url.data,
					image2_url=form.image2_url.data, 
					image3_url=form.image3_url.data)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live.')
		return redirect('index')
	return render_template('post.html', form=form)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user.id != post.user_id:
		return redirect(url_for('.index'))
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data 
		post.image1_url = form.image1_url.data
		post.image2_url = form.image2_url.data 
		post.image3_url = form.image3_url.data
		db.session.add(post)
		flash('The post has been updated')
		return redirect(url_for('.single_post', id=post.id))
	form.title.data = post.title
	form.body.data = post.body
	form.image1_url.data = post.image1_url
	form.image2_url.data = post.image2_url
	form.image3_url.data = post.image3_url
	return render_template('edit_post.html', form=form)


@main.route('/sign_s3/')
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
@main.route('/delete/<int:id>')
@login_required
def delete(id):
	post = Post.query.get(id)
	if post == None:
		flash('Post not found.')
		return redirect(url_for('.index'))
	if post.user_id != current_user.id:
		flash('You do not have rights to delete this post.')
		return redirect(url_for('.index'))
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted.')
	return redirect(url_for('.index'))

#Display the web app's about page
@main.route('/about')
def about():
	return render_template('about.html')


