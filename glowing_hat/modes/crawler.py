from random import randint

from glowing_hat.hue_sources.random_hue_source import RandomHueSource
from glowing_hat.mode import Mode
from glowing_hat.sorters.axis_manager import AxisManager


class Crawler(Mode):
    """Crawler."""

    def run(self):
        """Do the stuff."""
        self.hue_source = RandomHueSource()
        self.manager = AxisManager()

        while True:
            self.hat.sort_by_indeces(self.manager.get_random_sort())

            step = randint(1, self.conf["max-jump"])  # noqa: S311
            hue = self.hue_source.hue()

            for index, pixel in enumerate(self.hat.pixels):
                pixel["hue"] = hue
                pixel["value"] = 1.0
                self.hat.light_one(pixel)
                if index % step == 0:
                    self.hat.show()

            self.hat.show()
