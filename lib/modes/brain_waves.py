from collections import deque

from lib.arrangements.circle import Circle
from lib.hue_sources.time_based_hue_source import TimeBasedHueSource
from lib.mode import Mode


class BrainWaves(Mode):
    """Bands rising."""

    def configure(self):
        """Configure ourself."""
        self.hue_source = TimeBasedHueSource(
            seconds_per_rotation=self.conf["hue-seconds-per-rotation"]
        )
        self.values = deque()
        for i in range(self.conf["steps"]):
            self.values.append(i / self.conf["steps"])

        self.circle = Circle("z", "x")
        self.hat.sort_by_indeces(self.circle.next())

    def run(self):
        """Do the stuff."""
        self.configure()

        count = 0
        while True:
            hue = self.hue_source.hue()
            self.hat.apply_hue(hue)
            self.hat.apply_values(self.values)
            self.hat.light_up()

            self.values.rotate(self.conf["jump"])
            count += 1
            if count == self.conf["axis-rotate-at"]:
                self.hat.sort_by_indeces(self.circle.next())
                count = 0
