import time
from random import randint

from lib.hue_sources.time_based_hue_source import TimeBasedHueSource
from lib.mode import Mode
from lib.sorters.axis_manager import AxisManager


class Spots(Mode):
    """Spots."""

    def run(self):
        """Do the stuff."""
        self.hue_source = TimeBasedHueSource()
        self.manager = AxisManager()

        while True:
            sort = get_random_sort(10, len(self.hat), self.manager)

            hue = self.hue_source.hue()

            for index in sort[0:10]:
                pixel = self.hat.pixels[index]
                pixel["hue"] = hue
                pixel["value"] = 1.0
                self.hat.light_one(pixel)

            self.hat.show()

            time.sleep(1.7)


def get_random_sort(cube_size, hat_length, manager):
    """Get a random `sort`."""
    indeces = []
    while len(indeces) < hat_length:
        origin = [
            randint(-cube_size, cube_size) / 10,  # noqa: S311
            randint(-cube_size, cube_size) / 10,  # noqa: S311
            randint(-cube_size, cube_size) / 10,  # noqa: S311
        ]

        # at least one point must be `1.0` or the sorts can be shorter than 100
        origin[randint(0, 2)] = 1.0  # noqa: S311
        indeces = manager.get_sort_indeces(tuple(origin))

    return indeces
