import os
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from migrate.exceptions import DatabaseAlreadyControlledError

app = Flask(__name__, instance_relative_config=True, instance_path=os.environ['WANDER_PATH'])

app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('config.cfg', silent=True)
app.config.from_envvar('WANDER_CONFIG', silent=True)

api = restful.Api(app)
db = SQLAlchemy(app)

def start_jobs():
    import wander.worker
    wander.worker.start()

def init_db():
    import first_time
    try:
        first_time.create()
    except DatabaseAlreadyControlledError:
        pass


@app.before_first_request
def bootstrap():
    init_db()
    start_jobs()

# init routing
import views



