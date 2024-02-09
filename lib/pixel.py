# pylint: disable=C0103


class Pixel:
    """Class representing a single NeoPixel."""

    def __init__(self, data):
        """Construct."""
        self.data = data

    def greater_than(self, axis, value):
        """Is this Pixel's coord on `axis` >= `value`."""
        return self.data[axis] >= value

    def less_than(self, axis, value):
        """Is this Pixel's coord on `axis` < `value`."""
        try:
            return self.data[axis] < value
        except KeyError:
            return None

    def positive(self, axis):
        """Is this Pixel's `value` on `axis` >= than zero"""  # noqa: D400, D415
        return self.greater_than(axis, 0)

    def negative(self, axis):
        """Is this Pixel's `value` on `axis` < than zero"""  # noqa: D400, D415
        return self.less_than(axis, 0)

    def __getitem__(self, key):
        """Implement foo['bar']."""
        try:
            return self.data[key]
        except KeyError:
            return None

    # def is_inside_slice(self):
    # this is a prism with very large ends

    # def is_inside_cuboid(self):
    # this is a special case of the prism

    # def is_inside_sphere(self):

    # def is_inside_prism(self):
    # https://en.wikipedia.org/wiki/Prism_(geometry)
    # need face-corners, and angle?

    # def is_inside_tetrahedron(self):
