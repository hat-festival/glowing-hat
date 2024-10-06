from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode


class Solid(Mode):
    """Solid colours."""

    def configure(self):
        """Configure ourself."""
        self.hat.apply_value(1.0)
        self.hue_source = TimeBasedHueSource(
            seconds_per_rotation=self.conf["hue-seconds-per-rotation"]
        )

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            self.hat.apply_hue(self.hue_source.hue())
            self.hat.light_up()
