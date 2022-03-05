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
            return self.location[axis] < value
        except KeyError:
            print(self.index)

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
