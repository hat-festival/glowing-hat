import pickle
from random import randint

from lib.mode import Mode


class Crawler(Mode):
    """Crawler."""

    def run(self):
        """Do the stuff."""
        while True:
            origin = (
                randint(-10, 10) / 10,  # noqa: S311
                randint(-10, 10) / 10,  # noqa: S311
                randint(-10, 10) / 10,  # noqa: S311
            )
            # TODO wrap this somewhere
            self.hat.pixels = pickle.loads(self.redis.get(f"sorts:{origin!s}"))  # noqa: S301
            # self.hat.sort(choice(["x", "y", "z"]))
            # if random() < 0.5:
            #     self.hat.reverse()
            step = randint(1, self.data["max-jump"])  # noqa: S311
            clr = self.get_colour()

            for index, pixel in enumerate(self.hat.pixels):
                self.hat.light_one(pixel["index"], clr, auto_show=False)
                if index % step == 0:
                    self.hat.show()

            self.hat.show()
