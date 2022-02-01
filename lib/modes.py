from time import sleep

from lib.conf import conf
from lib.hat import Hat
from lib.redis_manager import RedisManager
from lib.tools import gamma_correct, hue_to_rgb


class Modes:
    """Some colour modes for the Hat."""

    def __init__(self, namespace="hat"):
        """Construct."""
        self.hat = Hat()
        self.redisman = RedisManager(namespace)
        self.redisman.populate()
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
        return self.redisman.retrieve("break-mode") == "false"

    def register_modes(self, modes):
        """Record our modes in Redis."""
        self.redisman.unset("modes")
        for mode in modes:
            self.redisman.push("modes", mode)

    def get_hue(self):
        """Retrieve the current hue for this namespace."""
        return float(self.redisman.retrieve("hue"))

    def run(self):
        """Run forever."""
        while True:
            mode = self.redisman.retrieve("mode")
            getattr(self, mode)()
            self.redisman.enter("break-mode", "false")
