import flask.ext.restless

from wander.app import app, db
from models import Trip, Point
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

def cols_trip(params):

    for o in params['objects']:
        del o['points']
    return params

trip_post = {
    "GET_MANY": [
        cols_trip
        ]
    }

manager.create_api(Trip, methods=['GET', 'POST', 'DELETE'], postprocessors=trip_post)
manager.create_api(Point, methods=['GET'])
