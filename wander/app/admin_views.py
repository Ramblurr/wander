from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin, BaseView, expose
from wander.app import app, api, db, admin
import models

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

class PKView(ModelView):
    column_display_pk = True

class TripView(PKView):
    column_hide_backrefs = False
    column_list = ('id', 'name', 'description', 'user')

admin.add_view(PKView(models.User, db.session))
admin.add_view(TripView(models.Trip, db.session))
admin.add_view(PKView(models.Point, db.session))
