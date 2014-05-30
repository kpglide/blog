import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
CSRF_ENABLED = True

"""In production, change secret key so that it originates from
an environment variable"""
SECRET_KEY = 'test_secret_key'

POSTS_PER_PAGE = 5