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

carto_trans = CartoTransaction(config.cartodb_api_key, config.cartodb_domain, config.cartodb_table)
for p in points:
    carto_trans.insert_point(p)
    mark_synced(p)

try:
    carto_trans.commit()
    db.session.commit()
except CartoDBException, e:
    print("carto commit failed", e)
    db.rollback()


