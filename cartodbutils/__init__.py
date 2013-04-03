from cartodb import CartoDBAPIKey

class CartoTransaction(object):

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
        resp = self.cl.sql(query)
        if self.debug:
            print query
            print resp

    def insert_point(self, point):
        insert = "insert into %s ( the_geom, happened_at, message ) values (ST_SetSRID(ST_Point(%s,%s), 4326), '%s', '%s');" % ( self.table, point.longitude, point.latitude, point.dateTime, point.message )
        self.queries.append(insert)



