import shelve
import contextlib

# Shity dbm doesn't support unicode strings

def _fix_key(key):
    return key.encode('utf-8')

def put(db_file, key, value):
    key = _fix_key(key)
    db = shelve.open(db_file)
    with contextlib.closing(db):
        db[key] = value

def exists(db_file, key):
    key = _fix_key(key)
    db = shelve.open(db_file)
    with contextlib.closing(db):
        return db.has_key(key)

def get(db_file, key):
    key = _fix_key(key)
    db = shelve.open(db_file)
    with contextlib.closing(db):
        return db[key]

def get_keys(db_file):
    db = shelve.open(db_file)
    with contextlib.closing(db):
        return db.keys()


