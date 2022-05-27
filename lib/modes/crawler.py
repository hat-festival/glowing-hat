from random import choice, randint, random

from lib.mode import Mode


class Crawler(Mode):
    """Crawler."""

    def run(self):
        """Do the stuff."""
        while True:
            self.hat.sort(choice(["x", "y", "z"]))
            if random() < 0.5:
                self.hat.reverse()
            step = randint(1, self.data["max-jump"])
            clr = self.get_colour()

            for index, pixel in enumerate(self.hat.pixels):
                self.hat.light_one(pixel["index"], clr, auto_show=False)
                if index % step == 0:
                    self.hat.show()

            self.hat.show()
