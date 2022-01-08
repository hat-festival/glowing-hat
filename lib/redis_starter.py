import redis

from lib.tools import make_key

defaults = {"hue": 0, "saturation": 1, "value": 1, "colour": "red", "mode": "flash"}


def initialise_redis(namespace="hat", flush=False):
    """Initialise Redis namespace."""
    rds = redis.Redis()

    if flush:
        for key in rds.scan_iter(f"{namespace}:*"):
            rds.delete(key)

    for key, value in defaults.items():
        if not rds.get(make_key(key, namespace)):
            rds.set(make_key(key, namespace), value)
