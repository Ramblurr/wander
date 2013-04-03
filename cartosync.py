from cartodbutils import CartoTransaction
from cartodb import CartoDBException
import datetime

from app import db, models
import config

now = datetime.datetime.now()

def mark_synced(point):
    entry = models.CartoDbSyncEntry()
    entry.point_id = point.id
    entry.timestamp = now

    db.session.add(entry)

# get list of un-synced points
synced = models.CartoDbSyncEntry.query.all()
synced_ids = [ p.point_id for p in synced ]


points = models.Point.query.filter(~models.Point.id.in_(synced_ids)).all()

print "Found %s unsynced points, syncing..." % (len(points))

carto_trans = CartoTransaction(config.cartodb_api_key, config.cartodb_domain, config.cartodb_table, debug=config.debug)
track_trip_ids = set()
for p in points:
    if p.point_type == models.Point.TypeCheckin:
        carto_trans.insert_point(p)
    elif p.point_type == models.Point.TypeTrack:
        track_trip_ids.add(p.trip_id)
    mark_synced(p)

print("%s trips need track path updating" % len(track_trip_ids))

for trip_id in track_trip_ids:
    track_points = models.Point.query.filter(models.Point.trip_id == trip_id and models.Point.point_type == models.Point.TypeTrack).order_by(db.asc(models.Point.dateTime)).all()
    coords = [ p.simple() for p in track_points ]
    carto_trans.update_line(trip_id, coords)

try:
    carto_trans.commit()
    db.session.commit()
except CartoDBException, e:
    print("carto commit failed", e)
    db.session.rollback()


