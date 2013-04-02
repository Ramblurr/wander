# Wander

An adventure tracking and visualization platform ala SPOT Adventures, but
completely customizable and 100% yours.

**Features**

* Automatically plot your adventure progress on a gorgeous map
* Grabs your SPOT checkins and tracking data
* Post messages and photos from your Android device (requires data)

### Components

1. SPOT Fetcher

    Periodically fetches the latest data from a SPOT GPS messenger data feed
    and stores it in a SQL database.

2. SQL Database

    Stores the raw spot data, as well as manual data uploaded from the Android app

3. REST API

    Exposes trip data via HTTP. Updates to trips can be submitted (from the
    Android app)

4. CartoDB syncher

    Periodically syncs the trip data with a cartodb table.

### Data

* **Points** - discreet location events with associated metadata (e.g., photo, message)
* **Paths** - collections of points interpreted as a path or route
* **Trips** - logical collections of points and paths with metadata (name)

**On Transforming SPOT data**

SPOT messages with `messageType` of `TRACK` are treated as points in a path.
All other messages are treated as waypoints displayed on the map.

**On cartodb syncing**

Paths are added as MultiLineStrings and all other points are added as single points.

The following columns are used:

message - string
happened_at - date
the_geom - lat,long or geojson repr


NOTES:
email in with
http://www.cloudmailin.com/
