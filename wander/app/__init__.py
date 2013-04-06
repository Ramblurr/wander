import os
import logging as log
from logging.handlers import RotatingFileHandler
from flask import Flask, g

from flask.ext.admin import Admin
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.openid import OpenID
from flask.ext.bootstrap import Bootstrap

from migrate.exceptions import DatabaseAlreadyControlledError


handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
handler.setLevel(log.INFO)

app = Flask(__name__, instance_relative_config=True, instance_path=os.environ['WANDER_PATH'])

app.config.from_object('wander.app.defaultconfig')
app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('config.cfg', silent=True)
app.config.from_envvar('WANDER_CONFIG', silent=True)
app.logger.addHandler(handler)

Bootstrap(app)
api = restful.Api(app)
admin = Admin(app, name = "Wander Admin")
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(app.config['TMP_DIR'], 'tmp'))

def start_jobs():
    import wander.worker
    wander.worker.start()

def init_db():
    import first_time
    if os.environ.has_key('WANDER_WIPE'):
        first_time.purge()
    try:
        first_time.create()
    except DatabaseAlreadyControlledError:
        pass


@app.before_first_request
def bootstrap():
    init_db()
    start_jobs()

# important settings
@lm.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


# init routing
import views
import login
import admin_views


