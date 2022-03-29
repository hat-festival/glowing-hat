import json
from random import random

import redis

from lib.tools import hue_to_rgb


class Custodian:
    """State manager."""

    def __init__(self, namespace="hat", conf=None):
        """Construct."""
        self.redis = redis.Redis()
        self.namespace = namespace
        self.conf = conf

    def populate(self, flush=False):
        """Insert initial data."""
        if flush:
            self.redis.flushall()

        if self.conf:
            for name, values in self.conf["hoops"].items():
                for value in values:
                    self.add_item_to_hoop(value, name)

            for name in self.conf["hoops"].keys():
                self.next(name)

            for name, _ in self.conf["colour-sets"].items():
                self.add_item_to_hoop(name, "colour-set")

            self.next("colour-set")

    def add_item_to_hoop(self, item, hoop):
        """Add an item to a hoop."""
        key = self.make_key(f"hoop:{hoop}")
        existing = list(map(lambda x: x.decode(), self.redis.lrange(key, 0, -1)))
        if item not in existing:
            self.redis.lpush(key, item)

    def next(self, thing):
        """Move the `next` item to the appropriate key."""
        key = self.make_key(thing)
        hoop_key = self.make_key(f"hoop:{thing}")

        next_item = self.redis.rpop(hoop_key).decode()
        self.redis.set(key, next_item)
        self.add_item_to_hoop(next_item, f"{thing}")

        if thing == "colour-set":
            self.load_colour_set(self.conf["colour-sets"][self.get("colour-set")])

    def get(self, key):
        """Get a value."""
        if key == "colour" and self.get("colour-source") == "wheel":
            hue = self.get("hue")
            if not hue:
                hue = 1.0
            return hue_to_rgb(hue)

        if key == "colour" and self.get("colour-source") == "random":
            return hue_to_rgb(random())

        # else:
        value = self.redis.get(self.make_key(key))
        if value:
            decoded = value.decode()
            try:
                return json.loads(decoded)
            except json.decoder.JSONDecodeError:
                return decoded

        return None

    def set(self, key, value):
        """Set a value."""
        self.redis.set(self.make_key(key), value)

    def load_colour_set(self, colours):
        """Load-in a colour-set."""
        key = self.make_key("hoop:colour")
        self.redis.delete(key)
        for triple in colours.values():
            self.add_item_to_hoop(json.dumps(triple), "colour")

        self.next("colour")

    def make_key(self, key):
        """Make compound key."""
        return f"{self.namespace}:{key}"
