from flask import make_response
from flask.ext.restful import Resource, Api, abort, reqparse
import json

from wander.app import app, api, db
import models

def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data, cls=models.TypeEncoder), code)
    resp.headers.extend(headers or {})
    return resp

api.representations['application/json'] = output_json
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class TripListResource(Resource):
    def get(self):
        return models.Trip.query.all()

    def post(self):
        args = parser.parse_args()
        trip = models.Trip(args['name'])
        db.session.add(trip)
        db.session.commit()
        return trip, 201


class TripResource(Resource):
    def get(self, trip_id):
        trip = models.Trip.query.filter_by(id=trip_id).first()
        if trip is None:
            return abort(404, message="Trip {} doesn't exist".format(trip_id))
        return trip

api.add_resource(TripListResource, '/trips')
api.add_resource(TripResource, '/trips/<string:trip_id>')
