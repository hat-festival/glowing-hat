import json

import redis

from lib.logger import logging
from lib.random_colour_source import RandomColourSource
from lib.tools import hue_to_rgb


class Custodian:
    """State manager."""

    def __init__(self, namespace="hat", conf=None):
        """Construct."""
        self.redis = redis.Redis()
        self.namespace = namespace
        self.conf = conf
        self.rcs = RandomColourSource()

    def populate(self, flush=False):  # noqa: FBT002
        """Insert initial data."""
        if flush:
            self.redis.flushall()

    def add_item_to_hoop(self, item, hoop):
        """Add an item to a hoop."""
        key = self.make_key(f"hoop:{hoop}")
        existing = list(  # noqa: C417
            map(lambda x: x.decode(), self.redis.lrange(key, 0, -1))
        )
        if item not in existing:
            self.redis.lpush(key, item)

    def next(self, thing):
        """Move the `next` item to the appropriate key."""
        hoop_key = self.make_key(f"hoop:{thing}")
        logging.debug(hoop_key)
        next_item = self.redis.rpop(hoop_key).decode()
        self.set(thing, next_item)
        self.add_item_to_hoop(next_item, f"{thing}")

    def get(self, key):
        """Get a value."""
        if key == "colour":
            hue = self.get("hue")
            if not hue:
                hue = 1.0
            return hue_to_rgb(hue)

        if key == "colour" and self.get("colour-source") == "random":
            return self.rcs.colour

        # else:
        value = self.redis.get(self.make_key(key))
        if value:
            decoded = value.decode()
            try:
                return json.loads(decoded)
            except json.decoder.JSONDecodeError:
                if decoded.lower() in ["frue", "false"]:
                    return decoded.lower() == "true"
                return decoded

        return None

    def set(self, key, value):
        """Set a value."""
        self.redis.set(self.make_key(key), str(value))

    def unset(self, key):
        """Unset something."""
        self.redis.delete(self.make_key(key))

    def rotate_until(self, hoop, value):
        """Rotate a hoop until the desired value is selected."""
        while self.get(hoop) != value:
            self.next(hoop)

    def make_key(self, key):
        """Make compound key."""
        return f"{self.namespace}:{key}"
