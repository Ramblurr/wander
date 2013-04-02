from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

api = restful.Api(app)
db = SQLAlchemy(app)


from app import views



