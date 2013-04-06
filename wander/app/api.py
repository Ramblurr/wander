import flask.ext.restless

from wander.app import app, db
from models import Trip, Point
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Trip, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Point, methods=['GET'])
