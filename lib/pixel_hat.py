import board
from neopixel import NeoPixel

from lib.pixel import Pixel
from lib.scaler import Scaler


class PixelHat(list):
    """Hat with pixels."""

    def __init__(self, locations="conf/locations.yaml"):  # pylint: disable=W0231
        self.locations = locations
        self.scaler = Scaler(locations)

        for location in self.scaler:
            self.append(Pixel(location))

        self.pixels = NeoPixel(board.D18, len(self), auto_write=False)

    def colour_indeces(self, indeces, colour):
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.pixels[index] = colour
        self.pixels.show()

    def light_one(self, index, colour):
        """Light up a single pixel."""
        self.pixels[index] = colour

    def off(self):
        """Turn all the lights off."""
        self.pixels.fill([0, 0, 0])
        self.pixels.show()

    def show(self):
        """Show our lights."""
        self.pixels.show()
