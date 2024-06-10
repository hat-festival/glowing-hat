from time import sleep

from glowing_hat.mode import Mode
from glowing_hat.tempo.tempo_pool import TempoPool
from glowing_hat.hue_sources.random_hue_source import RandomHueSource

class Tapper(Mode):
    """Tap."""

    def configure(self):
        """Configure ourself."""
        self.saturation = 1.0
        self.value = self.conf["base-value"]
        self.hue_source = RandomHueSource()
        self.tempo_pool = TempoPool(self)

    def run(self):
        """Do the work."""
        self.configure()
        self.hat.apply_hue(self.hue_source.hue())
        self.hat.apply_value(self.conf["base-value"])

        while True:
            self.hat.apply_saturation(self.saturation)
            self.hat.apply_value(self.value)
            self.hat.light_up()

    def trigger(self):
        """Spike the saturation."""
        self.saturation = 0.0
        self.value = 1.0
        self.hat.apply_hue(self.hue_source.hue())

    def reduce(self):
        """Constantly resaturating."""
        while True:
            if self.saturation < 1.0:
                self.saturation += self.conf["decay"]["amount"]
            if self.value > self.conf["base-value"]:
                self.value -= self.conf["decay"]["amount"]

            sleep(self.conf["decay"]["interval"])
