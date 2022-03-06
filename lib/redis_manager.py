import redis

from lib.conf import conf
from lib.oled import Oled
from lib.tools import hue_to_rgb, make_key


class RedisManager:
    """Construct."""

    def __init__(self, namespace="hat"):
        self.redis = redis.Redis()
        self.namespace = namespace
        self.oled = Oled(self)

    def populate(self, flush=False):
        """Insert initial data."""
        if flush:
            for key in self.redis.scan_iter(f"{self.namespace}:*"):
                self.redis.delete(key)

        for key, value in conf["redis-defaults"].items():
            if not self.redis.get(make_key(key, self.namespace)):
                self.redis.set(make_key(key, self.namespace), value)

    def get(self, key):
        """Get a value."""
        value = self.redis.get(make_key(key, self.namespace))
        if value:
            return value.decode()

        return None

    def get_colour(self):
        """Return an RGB triple based on the current `hue`."""
        return hue_to_rgb(float(self.get("hue")))

    def set(self, key, value):
        """Set a value."""
        self.redis.set(make_key(key, self.namespace), value)
        if key in conf["display-keys"]:
            self.oled.update()

    def lpush(self, key, value):
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
