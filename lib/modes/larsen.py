from lib.mode import Mode
from lib.tools import scale_colour
from time import sleep

class Larsen(Mode):  # pylint: disable=W0231
    """Larsen scanner."""

    def run(self):
        """Do the stuff."""
        self.sort_hat()

        while True:
            colour = self.get_colour()
            for index, frame in enumerate(self.frame_sets):
                if index % self.data["step"] == 0:
                    colours = list(map(lambda x: scale_colour(colour, x), frame))
                    for index, value in enumerate(colours):
                        self.hat.light_one(
                            self.hat[index]["index"], value, auto_show=False
                        )

                    self.hat.show()

            self.hat.reverse()
            sleep(self.data["delay"])
