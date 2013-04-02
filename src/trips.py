import uuid, json
import persistence as db
from config import trips_db

class Trip(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def save(self):
        db.put(trips_db, self.id, self)

    def default(self, o):
        return [o.id, o.name]

def new_id():
    return str(uuid.uuid4())

def fetch(id):
    try:
        return db.get(trips_db, id)
    except KeyError:
        return None

def fetch_all():
    keys = db.get_keys(trips_db)
    trips = [ fetch(id) for id in keys ]
    return trips


def add(name):
    id = new_id()
    trip = Trip(id, name)
    trip.save()
    return id, trip

def test():
    id = new_id()
    trip = Trip(id, "foobar")
    trip.save()

    for trip in fetch_all():
        print trip.name, trip.id

class TypeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Trip):
            return { "id": o.id, "name": o.name }
        return json.JSONEncoder.default(self, o)

if __name__ == '__main__':
    test()
