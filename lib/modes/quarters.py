import random
from time import sleep

from lib.mode import Mode


class Quarters(Mode):
    """Quarters."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.halves = {
            "front": list(filter(lambda w: w.positive("z"), self.hat)),
            "back": list(filter(lambda w: w.negative("z"), self.hat)),
            "left": list(filter(lambda w: w.positive("x"), self.hat)),
            "right": list(filter(lambda w: w.negative("x"), self.hat)),
        }

        self.quarters = {
            "front-left": list(set(self.halves["front"]) & set(self.halves["left"])),
            "front-right": list(set(self.halves["front"]) & set(self.halves["right"])),
            "back-left": list(set(self.halves["back"]) & set(self.halves["left"])),
            "back-right": list(set(self.halves["back"]) & set(self.halves["right"])),
        }

    def run(self):
        """Do the stuff."""
        while True:
            quarter = self.quarters[random.choice(list(self.quarters))]
            colour = self.get_colour()

            for light in quarter:
                self.hat.light_one(light["index"], colour, auto_show=False)

            self.hat.show()
            sleep(random.random())
