from lib.conf import conf
from lib.tools import is_pi

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


class Hat:
    """Hat with a grid of NeoPixels."""

    def __init__(self):
        """Construct."""
        self.length = conf["lights"]

        if is_pi():
            self.pixels = NeoPixel(board.D21, self.length, auto_write=False)  # nocov
        else:
            self.pixels = FakePixel(4)

    def light_one(self, index, colour):
        """Light up a single pixel."""
        self.pixels[index] = colour
        self.pixels.show()

    def light_all(self, colour):
        """Light up all the pixels."""
        self.pixels.fill(colour)
        self.pixels.show()

    def colour_indeces(self, indeces, colour):
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.pixels[index] = colour
        self.pixels.show()

    def off(self):
        """Turn all the lights off."""
        self.pixels.fill([0, 0, 0])
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
        print(f"Showing lights: {self!s}")
