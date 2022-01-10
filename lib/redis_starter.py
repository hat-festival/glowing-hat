import redis

from lib.conf import conf
from lib.tools import make_key


def initialise_redis(namespace="hat", flush=False):
    """Initialise Redis namespace."""
    rds = redis.Redis()

    if flush:
        for key in rds.scan_iter(f"{namespace}:*"):
            rds.delete(key)

    for key, value in conf["redis-defaults"].items():
        if not rds.get(make_key(key, namespace)):
            rds.set(make_key(key, namespace), value)
