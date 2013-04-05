from wander.cartodbutils import CartoTransaction
from cartodb import CartoDBException
import datetime

from wander.app import app, db, models
from wander.worker import WanderJob

class CartoSyncJob(WanderJob):
    now = datetime.datetime.now()

    def mark_synced(self, point):
        entry = models.CartoDbSyncEntry()
        entry.point_id = point.id
        entry.timestamp = self.now
        db.session.add(entry)

    def new_points(self):
        # get list of un-synced points
        synced = models.CartoDbSyncEntry.query.all()
        synced_ids = [ p.point_id for p in synced ]
        points = models.Point.query.filter(~models.Point.id.in_(synced_ids)).all()
        return points

    def prepare_carto(self, points):
        carto_trans = CartoTransaction(app.config['CARTODB_KEY'], app.config['CARTODB_DOMAIN'], app.config['CARTODB_TABLE'], debug=app.debug)
        track_trip_ids = set()

        # process points by type and collect track points
        for p in points:
            if p.point_type == models.PointType.checkin:
                carto_trans.insert_point(p)
            elif p.point_type == models.PointType.track:
                track_trip_ids.add(p.trip_id)
            self.mark_synced(p)

        # process collected track points into a line
        for trip_id in track_trip_ids:
            track_points = models.Point.query.filter(models.Point.trip_id == trip_id and models.Point.point_type == models.PointType.track).order_by(db.asc(models.Point.dateTime)).all()
            coords = [ p.simple() for p in track_points ]
            carto_trans.update_line(trip_id, coords)

        self.log("%s trips need track path updating" % len(track_trip_ids))
        return carto_trans

    def _run(self):
        points = self.new_points()
        if len(points) == 0:
            self.log("Found 0 new points. Finishing.")
            return
        else:
            self.log("Found %s unsynced points, syncing..." % (len(points)))
        carto_trans = self.prepare_carto(points)

        try:
            carto_trans.commit()
            db.session.commit()
        except CartoDBException, e:
            self.log("Error: carto commit failed", e)
            db.session.rollback()

