from colorsys import hsv_to_rgb

from lib.brightness_control import BrightnessControl
from lib.pixel import Pixel
from lib.scaler import Scaler
from lib.tools import gamma_correct, is_pi

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


# TODO: sort_by sets the default axis, which then sets the current "angle" on the pixels
# TODO: implement something like `map` to apply a list of things to the whole list


class PixelList:
    """A list of Pixels."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.pixels = list(map(Pixel, Scaler(locations)))

        if is_pi():
            self.lights = NeoPixel(
                board.D21, len(self.pixels), auto_write=False
            )  # nocov
            self.brightness_control = BrightnessControl()
            self.brightness_control.run()

        else:
            self.lights = FakeLights(len(self.pixels))
            self.brightness_control = FakeBrightnessControl()

    def light_up(self):
        """Light up our lights."""
        for pixel in self.pixels:
            self.lights[pixel["index"]] = gamma_correct(
                tuple(
                    int(x * 255)
                    for x in hsv_to_rgb(
                        pixel["hue"],
                        1,
                        pixel["value"] * self.brightness_control.factor.value,
                    )
                )
            )
        self.lights.show()

    def sort_by_indeces(self, indeces):
        """Sort by some arbitrary indeces."""
        self.pixels = [
            next(filter(lambda x: x["index"] == index, self.pixels))
            for index in indeces
        ]

    def __getitem__(self, index):
        """Implement `foo[bar]`."""
        return self.pixels[index]

    def __len__(self):
        """Implement `len()`."""
        return len(self.pixels)


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


class FakeBrightnessControl:
    """Fake brightness control for testing."""

    def __init__(self):
        """Construct."""
        self.factor = FakeFactor(1.0)


class FakeFactor:
    """Fake value thing."""

    def __init__(self, value):
        """Construct."""
        self.value = value