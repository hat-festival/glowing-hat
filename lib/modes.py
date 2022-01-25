from time import sleep

import redis

from lib.conf import conf
from lib.hat import Hat
from lib.redis_starter import initialise_redis
from lib.tools import gamma_correct, hue_to_rgb, make_key


class Modes:
    """Some colour modes for the Hat."""

    def __init__(self, namespace="hat"):
        """Construct."""
        initialise_redis()

        self.hat = Hat()
        self.redis = redis.Redis()
        self.namespace = namespace

        self.register_modes(["flash", "blend", "chase"])

    ###

    def flash(self):
        """Flash the lights on and off with a single colour."""
        if self.can_continue:
            self.hat.light_all(gamma_correct(hue_to_rgb(self.get_hue())))
            sleep(0.1)
            self.hat.off()
            sleep(0.1)

    def blend(self):
        """Recolour the lights gradually."""
        if self.can_continue:
            self.hat.light_all(hue_to_rgb(self.get_hue()))
            sleep(0.1)

    def chase(self):
        """Chase a light up the string."""
        for i in range(conf["lights"]):
            if self.can_continue:
                self.hat.off()
                self.hat.light_one(i, hue_to_rgb(self.get_hue()))
                sleep(0.05)
            else:
                return

    ###

    @property
    def can_continue(self):
        """Determine whether we should stop."""
        return (
            self.redis.get(make_key("break-mode", self.namespace)).decode() == "false"
        )

    def register_modes(self, modes):
        """Record our modes in Redis."""
        key = make_key("modes", self.namespace)
        self.redis.delete(key)
        for mode in modes:
            self.redis.lpush(key, mode)

    def get_hue(self):
        """Retrieve the current hue for this namespace."""
        return float(self.redis.get(make_key("hue", self.namespace)).decode())

    def run(self):
        """Run forever."""
        while True:
            mode = self.redis.get(make_key("mode", self.namespace)).decode()
            getattr(self, mode)()
            self.redis.set(make_key("break-mode", self.namespace), "false")
