from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin, BaseView, expose
from wander.app import app, api, db, admin
import models

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Trip, db.session))
admin.add_view(ModelView(models.Point, db.session))
