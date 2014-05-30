import os
import unittest
from datetime import datetime
import config
from config import basedir
from app import app, db
from app.models import User, Post

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.app.post('/admin', data={
			'username': username,
			'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
		
    def post(self, title, body):
        return self.app.post('/post', data={
			'title': title,
			'body': body
        }, follow_redirects=True)

    def create_user(self):
        u = User(username='testtest', password='password', role=1)
        db.session.add(u)
        db.session.commit()
		
    def create_post(self):
		self.create_user()
		u = User.query.first()
		p = Post(title='test_post', body='test_post_body', user_id=u.id)
		db.session.add(p)
		db.session.commit()

    def test_create_user(self):
        u = self.create_user()
        u2 = User.query.first()
        assert u2.username == 'testtest' and u2.password == 'password'

    def test_create_post(self):
        p = self.create_post()
        p2 = Post.query.first()
        assert p2.title == 'test_post' and p2.body == 'test_post_body'
		
    def test_home_page(self):
        response = self.app.get('/index')
        assert '<div id="post">' in response.data

    def test_about_page(self):
        response = self.app.get('/about')
        assert '<div id ="about_title">' in response.data		
	
    def test_login(self):
        self.create_user()
        response = self.login(username='testtest', password='password')
        assert 'Post' in response.data

    def test_invalid_login(self):
        response = self.login(username='invalid', password='invalidpassword')
        print response.data
        assert 'contact' in response.data
		
    def test_logout(self):
        self.create_user()
        self.login(username='testtest', password='password')
        response = self.logout()
        assert 'logged' in response.data
		
    def test_post_page(self):
        self.create_user()
        self.login(username='testtest', password='password')
        response = self.post(title='test_post', body='test_post_body')
        assert ('test_post' and 'test_post_body') in response.data

    def test_delete_post(self):
        self.create_user()
        self.login(username='testtest', password='password')
        self.post(title='test_post', body='test_post_body')
        p = Post.query.first()
        url = '/delete/{}'.format(p.id)
        response = self.app.get(url, follow_redirects=True)
        assert 'deleted' in response.data
		
		
if __name__ == '__main__':
    unittest.main()

