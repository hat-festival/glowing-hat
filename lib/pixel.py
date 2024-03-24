from collections import deque
from colorsys import hsv_to_rgb
from math import atan2, degrees

# TODO make some os these fields immutable

IMMUTABLE_FIELDS = ["x", "y", "z"]


class Pixel:
    """Class representing a single NeoPixel."""

    def __init__(self, data):
        """Construct."""
        self.data = data

        self.populate_hsv()
        self.calculate_rgb()
        self.calculate_angles()

    def populate_hsv(self):
        """Populate the HSV components with defaults as required."""
        for component in ["hue", "saturation", "value"]:
            if component not in self.data:
                self[component] = 1.0

    def calculate_rgb(self):
        """Calculate our RGB triple."""
        self["rgb"] = tuple(
            int(x * 255)
            for x in hsv_to_rgb(
                self.get("hue"), self.get("saturation"), self.get("value")
            )
        )

    def calculate_angles(self):
        """Set our angles."""
        axes = deque(["x", "y", "z"])
        self["angles"] = {}
        for _ in range(len(axes)):
            self["angles"][axes[0]] = angle_to_point(self[axes[1]], self[axes[2]])
            axes.rotate()

    def __getitem__(self, key):
        """Implement foo['bar']."""
        try:
            return self.data[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        """Implement foo['bar'] = baz."""
        if key not in IMMUTABLE_FIELDS:
            self.data[key] = value

            if key in ["hue", "saturation", "value"]:
                self.calculate_rgb()

    def get(self, key):
        """Return a default if we need it."""
        if key in self.data:
            return self[key]
        return 1.0

    def reset(self):
        """Reset our `s` and `v`."""
        self["saturation"] = self["value"] = 1.0


# https://stackoverflow.com/a/62482938
def angle_to_point(axis_0, axis_1):
    """Get the angle of this line with the horizontal axis."""
    theta = atan2(axis_1, axis_0)
    angle = degrees(theta)
    if angle < 0:
        angle = 360 + angle

    if angle == 0:
        angle = 360

    return angle
