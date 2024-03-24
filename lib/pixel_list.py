from lib.pixel import Pixel
from lib.scaler import Scaler
from lib.tools import is_pi

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


# TODO: sort_by sets the default axis, which then sets the current "angle" on the pixels
# TODO: run it through the normaliser
class PixelList:
    """A list of Pixels."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.pixels = list(map(Pixel, Scaler(locations)))

        if is_pi():
            self.lights = NeoPixel(
                board.D21, len(self.pixels), auto_write=False
            )  # nocov
        else:
            self.lights = FakeLights(len(self.pixels))

    def light_up(self):
        """Light up our lights."""
        self.lights = [pixel["rgb"] for pixel in self.pixels]

    def __getitem__(self, index):
        """Implement `foo[bar]`."""
        return self.pixels[index]


class FakeLights(list):
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
        # print(f"Showing lights: {str(self)}")
