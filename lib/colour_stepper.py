from collections import OrderedDict

import redis

from lib.tools import make_key

COLOURS = OrderedDict(
    {
        "red": 0,
        "yellow": 1 / 6,
        "green": 2 / 6,
        "cyan": 3 / 6,
        "blue": 4 / 6,
        "magenta": 5 / 6,
    }
)


class ColourStepper:
    """Step through the single colours."""

    def __init__(self, namespace="hat"):
        self.redis = redis.Redis()
        self.namespace = namespace

    def step(self):
        """Step to the next colour."""
        colour_key = make_key("colour", self.namespace)
        current_colour = self.redis.get(colour_key).decode()
        keys = list(COLOURS.keys())
        index = keys.index(current_colour)
        next_index = (index + 1) % len(keys)

        self.redis.set(make_key("hue", self.namespace), COLOURS[keys[next_index]])
        self.redis.set(colour_key, keys[next_index])
