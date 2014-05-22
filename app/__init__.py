from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
moment = Moment(app)

from app import views, models