from time import sleep

from lib.fft_pool import FFTPool
from lib.mode import Mode


class Equaliser(Mode):
    """Equalise."""

    def configure(self):
        """Configure ourself."""
        self.decay_amount = self.data["decay"]["amount"]
        self.decay_interval = self.data["decay"]["interval"]

        self.max_y = self.data["y"]["max"]
        self.default_y = self.data["y"]["default"]
        self.active_y = self.default_y

        self.fft_pool = FFTPool(self)

    def run(self):
        """Do the work."""
        self.configure()

        rotation = 90
        while True:
            self.hat.update_hues_from_angles(offset=rotation)
            rotation = (rotation + self.data["rotation"]) % 360

            self.hat.dim_pixels_greater_than_foo(
                self.data["scale-factor"], self.active_y, axis="y"
            )
            self.hat.light_up()

            rotation += self.data["rotation"]

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y = self.max_y

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y > self.default_y:
                self.active_y -= self.decay_amount
                sleep(self.decay_interval)
