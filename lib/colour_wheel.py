from time import sleep

import redis

from lib.tools import make_key


class ColourWheel:
    """Spin the `hue` wheel round and round."""

    def __init__(self, interval=0.01, namespace="hat"):
        """Construct."""
        self.interval = interval
        self.namespace = namespace
        self.redis = redis.Redis()

    @property
    def start_hue(self):
        """Get the initial hue."""
        key = make_key("hue", self.namespace)
        hue = self.redis.get(key)
        if not hue:
            self.redis.set(key, 0)

        hue = float(self.redis.get(key).decode())

        return hue

    def rotate(self, testing=False, steps=1000):
        """Spin the wheel."""
        offset = self.start_hue

        if testing:
            self.interval = 0

        while True:
            for i in range(steps):
                hue = ((i / 1000) + offset) % 1
                self.redis.set(make_key("hue", self.namespace), hue)
                sleep(self.interval)

            if testing:
                break
