import os
import unittest
import config
from config import basedir
from app import app, db
from app.models import User, Post
from flask import url_for

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
			'username':'testtest',
			'password':'password'
        }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_most_recent_post(self):
        val = self.app.get('/')
        assert 'About' in val.data

    def test_create_user(self):
        u = User(username='testtest', password='password', role=1)
        db.session.add(u)
        db.session.commit()
        u2 = User.query.first()
        assert u2.username == 'testtest' and u2.password == 'password'
		
    def test_home_page(self):
        response = self.app.get('/index')
        assert 'describing' in response.data
		
    def test_login(self):
        u = User(username='testtest', password='password', role=1)
        db.session.add(u)
        db.session.commit()
        response = self.login(username='testtest', password='password')
        assert 'Post' in response.data
	

if __name__ == '__main__':
    unittest.main()

