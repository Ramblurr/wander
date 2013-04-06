import json
from wander.app import db
from wander.app.decl_enum import DeclEnum

metadata = db.MetaData()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    trips = db.relationship('Trip', backref = 'user', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    points = db.relationship('Point', backref='trip', lazy='dynamic')

    def __repr__(self):
        return '<Trip %r>' % self.name

    def out(self):
        return { "name": self.name, "id": self.id }

class PointType(DeclEnum):
    track = 'track', 'Tracking Point'
    checkin = 'checkin', 'Check In Point'
    unknown = 'unknown', 'Point'

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    point_type = db.Column(PointType.db_type(), default=PointType.unknown, nullable=False)
    message = db.Column('message', db.Text(), default=u'')
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    dateTime = db.Column(db.Text(), nullable=False)
    unixTime = db.Column(db.Integer(), nullable=False)
    altitude = db.Column(db.Text(), nullable=True)

    def simple(self):
        return ( self.longitude, self.latitude )

    def __repr__(self):
        return '<Point %s,%s:%s (trip: %s)>' %(self.latitude, self.longitude, self.point_type, self.trip_id)

class CartoDbSyncEntry(db.Model):
    __tablename__ = "cartodb_log"
    id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'))
    timestamp = db.Column(db.DateTime)

class TypeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Trip):
            return o.out()
        return json.JSONEncoder.default(self, o)


