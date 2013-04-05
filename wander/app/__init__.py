import os
from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True, instance_path=os.environ['WANDER_PATH'])

app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('config.cfg', silent=True)
app.config.from_envvar('WANDER_CONFIG', silent=True)

api = restful.Api(app)
db = SQLAlchemy(app)

@app.before_first_request
def start_jobs():
    import wander.worker
    wander.worker.start()

# init routing
import views



