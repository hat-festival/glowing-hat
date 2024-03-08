from random import randint

from lib.logger import logging
from lib.mode import Mode
from lib.random_colour_source import RandomColourSource


class Crawler(Mode):
    """Crawler."""

    def run(self):
        """Do the stuff."""
        self.source = RandomColourSource()

        cube_size = 11
        while True:
            # origin = SortKey(
            #     randint(-cube_size, cube_size) / 10,
            #     randint(-cube_size, cube_size) / 10,
            #     randint(-cube_size, cube_size) / 10,
            # )
            origin = (
                randint(-cube_size, cube_size) / 10,  # noqa: S311
                randint(-cube_size, cube_size) / 10,  # noqa: S311
                randint(-cube_size, cube_size) / 10,  # noqa: S311
            )
            logging.debug(origin)
            self.from_sort(origin)

            step = randint(1, self.data["max-jump"])  # noqa: S311
            clr = self.source.colour

            for index, pixel in enumerate(self.hat.pixels):
                self.hat.light_one(pixel["index"], clr, auto_show=False)
                if index % step == 0:
                    self.hat.show()

            self.hat.show()
