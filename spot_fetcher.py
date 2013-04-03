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

    msg_t = m['messageType']
    if msg_t == 'TRACK':
        t = models.Point.TypeTrack
    elif msg_t == 'OK':
        t = models.Point.TypeCheckin
    else:
        t = None
        print('found unknown message type: %s' % msg_t)

    if t is not None:
        point.point_type = t
        db.session.add(point)

db.session.commit()

print "  Success. Imported %s messages" %( len(messages) )
