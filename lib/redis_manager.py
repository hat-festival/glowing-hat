import redis

from lib.conf import conf
from lib.tools import make_key
from lib.tools import hue_to_rgb


class RedisManager:
    """Construct."""

    def __init__(self, namespace="hat"):
        self.redis = redis.Redis()
        self.namespace = namespace

    def populate(self, flush=False):
        """Insert initial data."""
        if flush:
            for key in self.redis.scan_iter(f"{self.namespace}:*"):
                self.redis.delete(key)

        for key, value in conf["redis-defaults"].items():
            if not self.redis.get(make_key(key, self.namespace)):
                self.redis.set(make_key(key, self.namespace), value)

    def retrieve(self, key):
        """Get a value."""
        value = self.redis.get(make_key(key, self.namespace))
        if value:
            return value.decode()

        return None

    def fetch_colour(self):
        """Return an RGB triple based on the current `hue`."""
        return hue_to_rgb(float(self.retrieve("hue")))

    def enter(self, key, value):
        """Set a value."""
        self.redis.set(make_key(key, self.namespace), value)

    def push(self, key, value):
        """Delegate `lpush`."""
        self.redis.lpush(make_key(key, self.namespace), value)

    def range(self, key):
        """Delegate `lrange`."""
        return list(
            map(
                lambda x: x.decode(),
                self.redis.lrange(make_key(key, self.namespace), 0, -1),
            )
        )

    def unset(self, key):
        """Delegate `delete`."""
        self.redis.delete(make_key(key, self.namespace))
