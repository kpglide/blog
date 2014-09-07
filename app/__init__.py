from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import config

#Apply SQLAlchemy, Manager, Moment and Pagedown extension to app
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()

#Create an app and apply configuration settings from config.py
def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	moment.init_app(app)
	pagedown.init_app(app)

	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

if __name__ == '__main__':
	manager.run()