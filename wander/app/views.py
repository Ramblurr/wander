from flask import make_response
from flask.ext.restful import Resource, Api, abort, reqparse
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
import json

from wander.app import app, api, db, lm, oid
import models
from models import User

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


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    print user
    return render_template('index.html',
        title = 'Home',
        user = user)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        username = resp.nickname
        if username is None or username == "":
            username = resp.email.split('@')[0]
        user = User(username = username, email = resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
