from flask import Flask, make_response
from flask.ext import restful
from flask.ext.restful import Resource, Api, abort, reqparse
import json

import trips
from trips import Trip, TypeEncoder

def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data, cls=TypeEncoder), code)
    resp.headers.extend(headers or {})
    return resp

app = Flask(__name__)
api = Api(app)
api.representations['application/json'] = output_json

app.debug = True

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class TripListResource(Resource):
    def get(self):
        t = trips.fetch_all()
        return t

    def post(self):
        args = parser.parse_args()
        id, trip = trips.add(args['name'])
        return trip, 201


class TripResource(Resource):
    def get(self, trip_id):
        t = trips.fetch(trip_id)
        if t:
            return t
        abort(404, message="Trip {} doesn't exist".format(trip_id))

api.add_resource(TripListResource, '/trips')
api.add_resource(TripResource, '/trips/<string:trip_id>')

if __name__ == '__main__':
    app.run()
