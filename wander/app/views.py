from flask import make_response
from flask import render_template, g
from flask.ext.login import login_required
import json

from wander.app import app, api, db, lm
import models

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    print user
    return render_template('index.html',
        title = 'Home',
        user = user)

