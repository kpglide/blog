from flask import render_template, flash, url_for, redirect, request
from flask.ext.login import login_user
from . import auth
from .. models import User
from .forms import LoginForm

#Display admin page where registered users are able to login
@auth.route('/admin', methods=['GET', 'POST'])
def admin():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		else:
			flash('Sorry, you are not registered.  Please contact the site owner to register.')
	return render_template('auth/admin.html', form=form)