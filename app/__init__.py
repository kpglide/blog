from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment

#Create an app and apply configuration settings from config.py
app = Flask(__name__)
app.config.from_object('config')

#Apply SQLAlchemy and moment extension to app
db = SQLAlchemy(app)
moment = Moment(app)

from app import views, models