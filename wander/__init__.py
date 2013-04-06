import functools

def _obj_dump(obj):
    """
    Custom function for dumping objects to JSON, if obj has __json__ attribute
    or method defined it will be used for serialization

    :param obj:
    """
    if hasattr(obj, '__json__'):
        if callable(obj.__json__):
            return obj.__json__()
        else:
            return obj.__json__
    else:
        raise NotImplementedError

try:
    import json

    # extended JSON encoder for json
    class ExtendedEncoder(json.JSONEncoder):
        def default(self, obj):
            try:
                return _obj_dump(obj)
            except NotImplementedError:
                pass
            return json.JSONEncoder.default(self, obj)
    # monkey-patch JSON encoder to use extended version
    json.dumps = functools.partial(json.dumps, cls=ExtendedEncoder)
except ImportError:
    pass

try:
    import simplejson as json

    def extended_encode(obj):
        try:
            return _obj_dump(obj)
        except NotImplementedError:
            pass
        raise TypeError("%r is not JSON serializable" % (obj,))
    json.dumps = functools.partial(json.dumps, default=extended_encode)
except ImportError:
    pass
