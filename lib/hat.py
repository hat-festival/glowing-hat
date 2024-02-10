from lib.conf import conf
from lib.pixel import Pixel
from lib.scaler import Scaler
from lib.tools import is_pi, normalise

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


class Hat:
    """Hat with pixels."""

    def __init__(self, locations="conf/locations.yaml", auto_centre=False):  # noqa: FBT002, D107
        self.conf = conf
        self.locations = locations
        self.scaler = Scaler(locations, auto_centre=auto_centre)

        self.pixels = list(map(Pixel, self.scaler))

        if is_pi():
            self.lights = NeoPixel(
                board.D21, len(self.pixels), auto_write=False
            )  # nocov
        else:
            self.lights = FakeLights(len(self.pixels))

    def light_one(self, index, colour, auto_show=True):  # noqa: FBT002
        """Light up a single pixel."""
        self.lights[index] = normalise(
            colour, factor=self.conf["brightness-factor"]
        )

        if auto_show:
            self.show()

    def colour_indeces(self, indeces, colour, auto_show=True):  # noqa: FBT002
        """Apply a colour to a list of lights."""
        for index in indeces:
            self.lights[index] = normalise(
                colour, factor=self.conf["brightness-factor"]
            )

        if auto_show:
            self.show()

    def sort(self, axis):
        """Sort our pixels a long an axis."""
        self.pixels.sort(key=lambda w: w[axis])

    def illuminate(self, colours):
        """Apply a whole list of colours to ourself."""
        for index, colour in enumerate(colours):
            self.light_one(self.pixels[index]["index"], colour, auto_show=False)
        self.show()

    def off(self):
        """Turn all the lights off."""
        self.lights.fill((0, 0, 0))
        self.lights.show()

    def show(self):
        """Show our lights."""
        self.lights.show()

    @property
    def length(self):
        """How long are we."""
        return len(self.pixels)

    def reverse(self):
        """Turn ourself around."""
        self.pixels.reverse()


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
