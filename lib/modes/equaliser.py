from time import sleep

from lib.fft.fft_pool import FFTPool
from lib.mode import Mode


class Equaliser(Mode):
    """Equalise."""

    def configure(self):
        """Configure ourself."""
        self.active_y = self.conf["y"]["default"]
        self.fft_pool = FFTPool(self)

    def run(self):
        """Do the work."""
        self.configure()

        rotation = 90
        while True:
            self.hat.update_hues_from_angles(offset=rotation)
            rotation = (rotation + self.conf["rotation"]) % 360

            self.hat.dim_pixels_greater_than_foo(
                self.conf["scale-factor"], self.active_y, axis="y"
            )
            self.hat.light_up()

            rotation += self.conf["rotation"]

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y = self.conf["y"]["max"]

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y > self.conf["y"]["default"]:
                self.active_y -= self.conf["decay"]["amount"]
                sleep(self.conf["decay"]["interval"])
