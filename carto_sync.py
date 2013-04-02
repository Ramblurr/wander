from cartodb import CartoDBAPIKey, CartoDBException
from sqlalchemy.orm import aliased
import datetime

from app import db, models
import config

now = datetime.datetime.now()

class CartoTransaction(object):

    def __init__(self):
        self.cl = CartoDBAPIKey(config.cartodb_api_key, config.cartodb_domain)
        self.queries = []

    def commit(self):

        stmts = "\n".join(self.queries)
        query = "BEGIN;\n"
        query += stmts
        query += "COMMIT;\n"
        print query
        print self.cl.sql(query)

    def insert_point(self, point):
        insert = "insert into %s ( the_geom, happened_at, message ) values (ST_SetSRID(ST_Point(%s,%s), 4326), '%s', '%s');" % ( config.cartodb_table, point.longitude, point.latitude, point.dateTime, point.message )
        self.queries.append(insert)


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

carto_trans = CartoTransaction()
for p in points:
    carto_trans.insert_point(p)
    mark_synced(p)

try:
    carto_trans.commit()
    db.session.commit()
except CartoDBException, e:
    print("carto commit failed", e)
    db.rollback()


