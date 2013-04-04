from cartodb import CartoDBAPIKey
import json
import datetime

class CartoTransaction(object):

    _SQL_INSERT = "insert into %s ( the_geom, type, happened_at, message ) values( %s, %s, %s, %s);"

    def __init__(self, api_key, domain, table, debug = False):
        self.cl = CartoDBAPIKey(api_key, domain)
        self.table = table
        self.queries = []
        self.debug = debug

    def commit(self):

        stmts = "\n".join(self.queries)
        query = "BEGIN;\n"
        query += stmts
        query += "COMMIT;\n"
        if self.debug:
            print query
        resp = self.cl.sql(query)
        if self.debug:
            print resp

    def _craft_insert(self, the_geom, event_type, happened_at, message):
        if happened_at is None:
            happened_at = ''
        if message is None:
            message = ''

        def quote(s):
            return "'" + s + "'"

        return self._SQL_INSERT % (self.table, the_geom , quote(event_type), quote(happened_at), quote(message))

    def insert_point(self, point):
        the_geom = "ST_SetSRID(ST_Point(%s,%s), 4326)" %(point.longitude, point.latitude)
        insert = self._craft_insert(the_geom, "checkin", point.dateTime, point.message)
        self.queries.append(insert)

    def update_line(self, trip_id, coords):
        geojson = json.dumps({ "type" : "MultiLineString", "coordinates": [coords] })
        the_geom = "ST_SetSRID(ST_GeomFromGeoJSON('%s'), 4326)" % (geojson)
        insert = self._craft_insert(the_geom, "track", str(datetime.datetime.now()), None)
        self.queries.append(insert)




