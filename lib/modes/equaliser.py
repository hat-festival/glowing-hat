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
        """Do the work."""
        self.configure()

        rotation = 90
        while True:
            for pixel in self.hat.pixels:  # TODO abstract this out for general use?
                pixel["angle"] = (angle(pixel["x"], pixel["z"]) - rotation) % 360
                pixel["hue"] = pixel["angle"] / 360
            rotation = (rotation + self.data["rotation"]) % 360

            self.from_list(
                brighten_pixels_less_than_y(
                    self.hat.pixels, self.active_y, self.data["scale-factor"]
                )
            )

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y = self.max_y

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y > self.default_y:
                self.active_y -= self.decay_amount
                sleep(self.decay_interval)


# TODO find new general home for this
def brighten_pixels_less_than_y(pixels, y_value, scale_factor):
    """Colour-scale some pixels."""
    lights = []
    for pixel in pixels:
        colour = hue_to_rgb(pixel["hue"])
        if pixel["y"] < y_value:
            lights.append(colour)
        else:
            lights.append(scale_colour(colour, scale_factor))

    return lights
