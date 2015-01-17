#Placeholder selenium test file.  Need to re-write this and develop 
#some sensible tests here.

import re
import unittest
import threading
from selenium import webdriver
from app import create_app, db
from app.models import User, Post

class SeleniumTestCase(unittest.TestCase):
	client = None

	@classmethod
	def setUpClass(cls):
		#start Firefox
		try:
			cls.client = webdriver.Firefox()
		except:
			pass

		if cls.client:
			#create the application
			cls.app = create_app('testing')
			cls.app_context = cls.app.app_context()
			cls.app_context.push()

			#suppress logging to keep unitteset output clean
			import logging
			logger = logging.getLogger('werkzeug')
			logger.setLevel("ERROR")

			#create database with fake user and post
			db.create_all()

			u = User(username='testtest', password='password', role=1)
			db.session.add(u)

			p = Post(title='test_post', body='test_post_body', user_id=u.id)
			db.session.add(p)
			db.session.commit()

			#start the Flask server in a thread
        	threading.Thread(target=cls.app.run).start()

	@classmethod
	def tearDownClass(cls):
		if cls.client:
			#stop the flask server and the browser
			cls.client.get('http://localhost:5000/shutdown')
			cls.client.close()

			#destroy database
			db.drop_all()
			db.session.remove()

			#remove app context
			cls.app_context.pop()

	def setUp(self):
		if not self.client:
			self.skipTest('Web browser not available')

	def tearDown(self):
		pass

	def test_login_and_post(self):
		
		#navigate to home
		self.client.get('http://localhost:5000/')
		self.assertTrue(re.search('technology', self.client.page_source))

		#navigate to login page
		self.client.find_element_by_link_text('Admin Login').click()
		self.assertTrue('Registered' in self.client.page_source)

		#login
		self.client.find_element_by_id('username').send_keys('testtest')
		self.client.find_element_by_id('password').send_keys('password')
		self.client.find_element_by_id('login_form_submit').click()
		self.assertTrue('<div id="post">' in self.client.page_source)

		#navigate to post page
		self.client.find_element_by_link_text('Post').click()
		self.assertTrue('Create a Post' in self.client.page_source)

		#preview body
		self.client.find_element_by_class_name('flask-pagedown-input').send_keys('test_post_body')
		preview = self.client.find_element_by_class_name('flask-pagedown-preview')
		self.assertTrue('test_post_body' in preview.text)

		#complete post and submit it
		self.client.find_element_by_id('title_input').send_keys('test_post_title')
		self.client.find_element_by_id('image1_url').\
				send_keys('https://kpglideblogimages.s3.amazonaws.com/IMG_5232.jpg')
		self.client.find_element_by_id('post_form_submit').click()
		self.assertTrue(('test_post_title' in self.client.page_source)\
						and ('test_post_body' in self.client.page_source)\
						and ('https://kpglideblogimages.s3.amazonaws.com/IMG_5232.jpg'\
						in self.client.page_source)
						)