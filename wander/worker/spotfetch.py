from spotpersist import parse_json, sql
from wander.app import app, db, models

from wander.worker import WanderJob

class SpotFetchJob(WanderJob):
    def __init__(self, json_file, archive_db, *args, **kwargs):
        WanderJob.__init__(self, *args, **kwargs)
        self.json_file = json_file
        self.archive_db = archive_db

    def parse_data(self):

        try:
            with open(self.json_file, 'r') as data:
                metadata, messages = parse_json(data)
                return metadata, messages
        except IOError, e:
            self.debug("Error parsing data: %s " % (e))
            return None, None

    def init_archive(self):
        sql.init_db(self.archive_db)

    def populate_archive(self, messages):
        sql.populate(messages, update = True)
        self.debug("  Success. Archived %s messages" % (len(messages)))

    def import_messages(self, messages):
        new_messages = filter(lambda msg: len(models.Point.query.filter_by(unixTime=msg['unixTime']).all()) == 0 , messages)
        self.debug("Importing %s new messages" %(len(new_messages)))
        for m in new_messages:
            point = models.Point()
            point.trip_id = app.config['ACTIVE_TRIP']
            point.latitude = m['latitude']
            point.longitude = m['longitude']
            point.altitude = m['altitude']
            point.dateTime = m['dateTime']
            point.unixTime = m['unixTime']
            if m.has_key('messageContent'):
                point.message = m['messageContent']

            msg_t = m['messageType']
            if msg_t == 'TRACK':
                t = models.PointType.track
            elif msg_t == 'OK':
                t = models.PointType.checkin
            else:
                t = None
                self.debug('found unknown message type: %s' % msg_t)

            if t is not None:
                point.point_type = t
                db.session.add(point)

        db.session.commit()

    def _run(self):
        metadata, messages = self.parse_data()
        if metadata is None:
            return
        self.init_archive()
        self.populate_archive(messages)
        self.import_messages(messages)




