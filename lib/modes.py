from time import sleep

import redis

from lib.hat import Hat
from lib.redis_starter import initialise_redis
from lib.tools import gamma_correct, hue_to_grb, make_key


class Modes:
    """Some colour modes for the Hat."""

    def __init__(self, namespace="hat"):
        """Construct."""
        initialise_redis()

        self.hat = Hat()
        self.redis = redis.Redis()
        self.namespace = namespace
        self.interval = 0.1

    def flash(self):
        """Flash the lights on and off with a single colour."""
        self.hat.light_all(gamma_correct(hue_to_grb(self.get_hue())))
        sleep(self.interval)
        self.hat.off()
        sleep(self.interval)

    def blend(self):
        """Recolour the lights every `interval` seconds."""
        self.hat.light_all(hue_to_grb(self.get_hue()))
        sleep(self.interval)

    def get_hue(self):
        """Retrieve the current hue for this namespace."""
        return float(self.redis.get(make_key("hue", self.namespace)).decode())

    def run(self):
        """Run forever."""
        mode = self.redis.get(make_key("mode", self.namespace)).decode()
        while True:
            getattr(self, mode)()
            mode = self.redis.get(make_key("mode", self.namespace)).decode()
