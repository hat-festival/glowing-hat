import platform
from pathlib import Path

import yaml

if "arm" in platform.platform():  # nocov
    import board
    from neopixel import NeoPixel


class Hat:
    """Hat with a grid of NeoPixels."""

    def __init__(self):
        """Construct."""
        self.conf = yaml.safe_load(Path("conf/conf.yaml").read_text(encoding="UTF-8"))
        self.length = self.conf["lights-count"]

        if "arm" in platform.platform():
            self.pixels = NeoPixel(board.D18, self.length, auto_write=False)  # nocov
        else:
            self.pixels = FakePixel(self.length)

    def light_one(self, index, colour):
        """Light up a single pixel."""
        self.pixels[index] = colour
        self.pixels.show()

    def light_all(self, colour):
        """Light up all the pixels."""
        self.pixels.fill(colour)
        self.pixels.show()

    def colour_indeces(self, colour, indeces):
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.pixels[index] = colour
        self.pixels.show()


class FakePixel(list):
    """Fake NeoPixels for testing."""

    def __init__(self, length):  # pylint: disable=W0231
        """Construct."""
        self.length = length
        for _ in range(self.length):
            self.append((0, 0, 0))

    def __setitem__(self, index, value):
        """Override [i] = foo."""

    def fill(self, colour):
        """Pretend to fill the pixels."""
        for index, _ in enumerate(self):
            self[index] = colour
