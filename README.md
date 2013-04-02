# Wander

An adventure tracking and visualization platform. Wander is an alternative to
SPOT Adventures; completely customizable and 100% yours.

*WANDER IS UNDER DEVELOPMENT*

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

    Syncs geo data with a [cartodb](http://cartodb.com) table.

### Data

* **Points** - discreet location events with associated metadata (e.g., photo, message)
* **Paths** - collections of points interpreted as a path or route
* **Trips** - logical collections of points and paths with metadata (name)

**On Transforming SPOT data**

SPOT messages with `messageType` of `TRACK` are treated as points in a path.
All other messages are treated as waypoints displayed on the map.

**On Cartodb Syncing**

Paths are added as MultiLineStrings and all other points are added as single points.

The following columns are used:

* message - string
* happened_at - date
* the_geom - lat,long or geojson repr

## Depdendenices

Everything in requirements.pip, just use `pip install requirements.pip` as well
as [spot-persist](https://github.com/Ramblurr/spot-persist)

## License & Custom Work

This project is licensed under the AGPL v3.

If you want a customized version of Wander for your adventure or expedition,
email me (me@caseylink.com). I am available for freelance and consulting
projects.

## Contributions

Bug reports, suggestions, and patches are welcome! Please use the github issue
tracker.

