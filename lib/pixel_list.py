from lib.brightness_control import BrightnessControl
from lib.pixel import Pixel
from lib.scaler import Scaler
from lib.tools import is_pi

if is_pi():  # nocov
    import board
    from neopixel import NeoPixel


# TODO: sort_by sets the default axis, which then sets the current "angle" on the pixels
# TODO: have the normaliser trigger a full rescaling when it adjusts?


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

        else:
            self.lights = FakeLights(len(self.pixels))
            self.brightness_control = FakeBrightnessControl()

    def light_up(self):
        """Light up our lights."""
        self.lights = [pixel["rgb"] for pixel in self.pixels]

    def __getitem__(self, index):
        """Implement `foo[bar]`."""
        return self.pixels[index]

    def trigger_rescale(self):
        """Called by brightness_controller."""  # noqa: D401
        for pixel in self.pixels:
            pixel.scale(
                self.brightness_control.factor
            )  # this might need to be a `Value`


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
        self.factor = 0.5

    # def normalise(self, triple):
    #     """Normalise a colour."""
    #     factor = max(self.factor, 0)
    #     return tuple(int(x * factor) for x in triple)
