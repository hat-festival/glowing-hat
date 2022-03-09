# noqa
from lib.mode import Mode


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        self.name = "bands"
        super().__init__(hat, self.name)

    def run(self):
        """Do the stuff."""
        self.hat.off()

        while True:

            for i in range(-10, 11, 1):
                increment = i / 10
                print(increment)

                for j in range(self.conf["modes"][self.name]["count"]):
                    lights = list(
                        filter(
                            lambda w: w.less_than(
                                self.axis,
                                increment - self.conf["modes"][self.name]["width"] * j,
                            ),
                            self.hat,
                        )
                    )
                    band = list(map(lambda x: x["index"], lights))
                    self.hat.colour_indeces(
                        band,
                        self.conf["colours"][
                            list(self.conf["colours"].keys())[(j * 2)]
                        ],
                        auto_show=False,
                    )

                self.hat.show()
                # sleep(0.01)
