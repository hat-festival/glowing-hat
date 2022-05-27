import json
from random import random

import redis

from lib.conf import conf
from lib.tools import hue_to_rgb


class Custodian:
    """State manager."""

    def __init__(self, namespace="hat", conf=None):
        """Construct."""
        self.redis = redis.Redis()
        self.namespace = namespace
        self.conf = conf
        self.rcs = RandomColourSource()

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
        hoop_key = self.make_key(f"hoop:{thing}")
        next_item = self.redis.rpop(hoop_key).decode()
        self.set(thing, next_item)
        self.add_item_to_hoop(next_item, f"{thing}")

    def get(self, key):
        """Get a value."""
        if key == "colour" and self.get("colour-source") == "wheel":
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
        if key == "colour-set":
            self.load_colour_set(self.conf["colour-sets"][self.get("colour-set")])

    def unset(self, key):
        """Unset something."""
        self.redis.delete(self.make_key(key))

    def rotate_until(self, hoop, value):
        """Rotate a hoop until the desired value is selected."""
        while not self.get(hoop) == value:
            self.next(hoop)

    def load_colour_set(self, colours):
        """Load-in a colour-set."""
        key = self.make_key("hoop:colour")
        self.redis.delete(key)
        for triple in colours.values():
            self.add_item_to_hoop(json.dumps(triple), "colour")

        self.next("colour")

    def reset_colour_sources(self, sources):
        """Load-in a list of valid colour-sources."""
        self.unset("hoop:colour-source")
        for source in sources:
            self.add_item_to_hoop(source, "colour-source")

    def make_key(self, key):
        """Make compound key."""
        return f"{self.namespace}:{key}"


class RandomColourSource:
    """Generate spaced-out random colours."""

    def __init__(self):
        """Construct."""
        self.conf = conf
        self.hue = self.next_hue = random()

    @property
    def colour(self):
        """Get a colour."""
        while (
            abs(self.hue - self.next_hue) < self.conf["random-colour"]["hue-distance"]
        ):
            self.next_hue = random()

        self.hue = self.next_hue

        return hue_to_rgb(self.hue)
