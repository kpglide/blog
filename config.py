import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
CSRF_ENABLED = True
SECRET_KEY = 'some-days-you-just-smoke'
POSTS_PER_PAGE = 5