import json
from app import db

metadata = db.MetaData()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    points = db.relationship('Point', backref='trip', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Trip %r>' % self.name

    def out(self):
        return { "name": self.name, "id": self.id }


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    message = db.Column('message', db.Text(), default=u'')
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    dateTime = db.Column(db.Text(), nullable=False)
    altitude = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return '<Point %s,%s:%s (trip: %s)>' %(self.latitude, self.longitude, self.message, self.trip_id)



class TypeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Trip):
            return o.out()
        return json.JSONEncoder.default(self, o)


