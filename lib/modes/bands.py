from math import ceil
from random import random
from lib.tools import hue_to_rgb
from lib.conf import conf
from lib.mode import Mode


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

        if self.invert:
            self.hat.reverse()

        self.jump = self.conf["modes"]["bands"]["jump"]

    def run(self):
        """Do the stuff."""
        colours_index = 0
        while True:
            # colour = self.redisman.get_colour()
            colour = hue_to_rgb(random())
            for i in range(ceil(len(self.hat) / self.jump)):
                for j in range(self.jump):
                    try:
                        self.hat.light_one(
                            self.hat[i * self.jump + j]["index"],
                            colour,
                            auto_show=False,
                        )
                    except IndexError:
                        pass
                self.hat.show()

                # try:
                #     self.hat.light_one(
                #     self.hat[i * self.jump + j - 10]["index"],
                #         [0, 0, 0],
                #         auto_show=False,
                #     )
                #     self.hat.show()
                # except IndexError:
                #     pass 

            colours_index = (colours_index + 1) % 6
