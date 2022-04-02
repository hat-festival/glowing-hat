from math import ceil
from time import sleep

from lib.mode import Mode
from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.jump = self.data["jump"]
        self.width = self.data["width"]

    def run(self):
        """Do the stuff."""
        self.sort_hat()

        while True:
            colour = self.get_colour()
            for i in range(ceil(len(self.hat) / self.jump) + 10):
                for j in range(self.jump):
                    try:
                        self.hat.light_one(
                            self.hat[i * self.jump + j]["index"],
                            colour,
                            auto_show=False,
                        )
                    except IndexError:
                        pass

                    try:
                        tail_index = i * self.jump + j - self.width
                        if tail_index >= 0:
                            self.hat.light_one(
                                self.hat[tail_index]["index"],
                                scale_colour(colour, self.data["fade-factor"]),
                                auto_show=False,
                            )
                    except IndexError:
                        pass

                self.hat.show()

            sleep(self.data["delay"])

            self.hat.reverse()
