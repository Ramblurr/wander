import os
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True, instance_path=os.environ['WANDER_PATH'])
app.config.from_pyfile('config.cfg')

api = restful.Api(app)
db = SQLAlchemy(app)


import views


