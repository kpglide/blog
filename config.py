import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRETKEY') or 'secret'

POSTS_PER_PAGE = 5