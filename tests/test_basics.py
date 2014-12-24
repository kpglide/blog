import unittest
from datetime import datetime
from flask import current_app
from app import create_app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing') 
        self.app_context = self.app.app_context()    
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)  
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/admin', data={
			'username': username,
			'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
		
    def post(self, title, body):
        return self.client.post('/post', data={
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
        assert u2.username == 'testtest' and u2.verify_password('password') == True

    def test_create_post(self):
        p = self.create_post()
        p2 = Post.query.first()
        assert p2.title == 'test_post' and p2.body == 'test_post_body'
		
    def test_home_page(self):
        response = self.client.get('/index')
        assert '<div id="post">' in response.data

    def test_about_page(self):
        response = self.client.get('/about')
        assert '<div id ="about_title">' in response.data		
	
    def test_login(self):
        self.create_user()
        response = self.login(username='testtest', password='password')
        assert 'Post' in response.data

    def test_invalid_login(self):
        response = self.login(username='invalid', password='invalidpassword')
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
        response = self.client.get(url, follow_redirects=True)
        assert 'deleted' in response.data

    def test_password_setter(self):
        u = User(username='dog', password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(username='dog', password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(username='dog', password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(username='dog', password='cat')
        u2 = User(username='dog2', password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)


		
		
if __name__ == '__main__':
    unittest.main()

