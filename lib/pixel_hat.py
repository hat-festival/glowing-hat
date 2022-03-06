import platform

from lib.pixel import Pixel
from lib.scaler import Scaler

if "arm" in platform.platform():  # nocov
    import board
    from neopixel import NeoPixel


class PixelHat(list):
    """Hat with pixels."""

    def __init__(self, locations="conf/locations.yaml"):  # pylint: disable=W0231
        self.locations = locations
        self.scaler = Scaler(locations)

        for location in self.scaler:
            self.append(Pixel(location))

        if "arm" in platform.platform():
            self.pixels = NeoPixel(board.D18, len(self), auto_write=False)  # nocov
        else:
            self.pixels = FakePixel(4)

    def colour_indeces(self, indeces, colour):
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.pixels[index] = colour
        self.pixels.show()

    def off(self):
        """Turn all the lights off."""
        self.pixels.fill([0, 0, 0])
        self.pixels.show()

    def show(self):
        """Show our lights."""
        self.pixels.show()


class FakePixel(list):
    """Fake NeoPixels for testing."""

    def __init__(self, length):  # pylint: disable=W0231
        """Construct."""
        self.length = length
        for _ in range(self.length):
            self.append((0, 0, 0))

    def fill(self, colour):
        """Pretend to fill the pixels."""
        for index, _ in enumerate(self):
            self[index] = colour

    def show(self):
        """Pretend to show the lights."""
        print(f"Showing lights: {str(self)}")
