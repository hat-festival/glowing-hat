from time import sleep

from glowing_hat.fft.fft_pool import FFTPool
from glowing_hat.mode import Mode


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

            for pixel in self.hat.pixels:
                if pixel["y"] >= self.active_y:
                    pixel["value"] = self.conf["scale-factor"]
                else:
                    pixel["value"] = 1.0

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
