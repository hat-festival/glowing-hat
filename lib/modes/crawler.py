from random import randint

from lib.hue_sources.random_hue_source import RandomHueSource
from lib.mode import Mode
from lib.sorters.axis_manager import AxisManager


class Crawler(Mode):
    """Crawler."""

    def run(self):
        """Do the stuff."""
        self.hue_source = RandomHueSource()
        self.manager = AxisManager()

        while True:
            self.hat.sort_by_indeces(
                get_random_sort(self.conf["cube-size"], len(self.hat), self.manager)
            )

            step = randint(1, self.conf["max-jump"])  # noqa: S311
            hue = self.hue_source.hue()

            for index, pixel in enumerate(self.hat.pixels):
                pixel["hue"] = hue
                pixel["value"] = 1.0
                self.hat.light_one(pixel)
                if index % step == 0:
                    self.hat.show()

            self.hat.show()


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
        indeces = manager.get_sort(tuple(origin))

    return indeces
