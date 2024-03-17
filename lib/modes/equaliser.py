from time import sleep

from lib.fft_pool import FFTPool
from lib.mode import Mode
from lib.renderers.sweeper import angle  # TODO rehome this to tools?
from lib.tools import hue_to_rgb, scale_colour


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
        """Do the sork."""
        self.configure()

        rotation = 90
        print(self.data)
        while True:
            self.hues = []
            for pix in self.hat.pixels:
                pix["angle"] = (angle(pix["x"], pix["z"]) - rotation) % 360
                pix["hue"] = pix["angle"] / 360
            rotation = (rotation + self.data["rotation"]) % 360

            lights = []
            for pixel in self.hat.pixels:
                colour = hue_to_rgb(pixel["hue"])
                if pixel["y"] < self.active_y:
                    lights.append(colour)
                else:
                    lights.append(scale_colour(colour, self.data["scale-factor"]))

            self.from_list(lights)

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y = self.max_y

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y > self.default_y:
                self.active_y -= self.decay_amount
                sleep(self.decay_interval)
