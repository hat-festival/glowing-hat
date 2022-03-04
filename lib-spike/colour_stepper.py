from collections import OrderedDict

from lib.redis_manager import RedisManager

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
        self.redisman = RedisManager(namespace)

    def step(self):
        """Step to the next colour."""
        keys = list(COLOURS.keys())
        index = keys.index(self.redisman.retrieve("colour"))
        next_index = (index + 1) % len(keys)

        self.redisman.enter("hue", COLOURS[keys[next_index]])
        self.redisman.enter("colour", keys[next_index])
