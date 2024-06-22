from time import sleep

from glowing_hat.mode import Mode
from glowing_hat.tempo.tempo_pool import TempoPool

class Tapper(Mode):
    """Tap."""

    def configure(self):
        """Configure ourself."""
        self.value = self.conf["base-value"]
        self.tempo_pool = TempoPool(self)

    def run(self):
        """Do the work."""
        self.configure()
        self.hat.apply_hue(self.conf["hues"]["high"])

        while True:
            self.hat.apply_value(self.value)
            self.hat.light_up()

    def trigger_high(self):
        """Spike."""
        self.value = 1.0
        self.hat.apply_hue(self.conf["hues"]["high"])

    def trigger_low(self):
        """Spike."""
        self.value = 1.0
        self.hat.apply_hue(self.conf["hues"]["low"])

    def reduce(self):
        """Constantly resaturating."""
        while True:
            if self.value > self.conf["base-value"]:
                self.value -= self.conf["decay"]["amount"]

            sleep(self.conf["decay"]["interval"])
