from spotpersist import parse_json, sql

from app import db, models
import config

print "++ Archiving SPOT json data"

data = open(config.spot_data, 'r')
metadata, messages = parse_json(data)

#sql.debug = True
sql.init_db('sqlite:///%s' % (config.spot_message_db))
sql.populate(messages, True)

print "  Success. Archived %s messages" % (len(messages))

print "++ Adding to trip database"

for m in messages:
    point = models.Point()
    point.trip_id = config.active_trip_id
    point.latitude = m['latitude']
    point.longitude = m['longitude']
    point.altitude = m['altitude']
    point.dateTime = m['dateTime']

    if m.has_key('messageContent'):
        point.message = m['messageContent']

    db.session.add(point)

db.session.commit()

print "  Success. Imported %s messages" %( len(messages) )


for p in models.Point.query.all():
    print p
