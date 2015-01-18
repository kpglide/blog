import os
from app import create_app, db
from app.models import User, Post
from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate, MigrateCommand, upgrade

#Create an app and apply configuration settings from config.py
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

#Make a shell context which automatically imports database and
#models for use within the python shell

def make_shell_context():
	return dict(app=app, db=db, User=User, Post=Post)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	"""Run the unit tests"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
	"""Run deployment tasks"""

	#migrate database to latest revision
	upgrade()

if __name__ == '__main__':
	manager.run()