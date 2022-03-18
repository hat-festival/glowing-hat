import pickle
from pathlib import Path

from lib.pixel_hat import PixelHat


class Band(list):
    """Individual Band sequence."""

    def __init__(self, width, axis, direction, steps=200, hat=None):
        """Construct."""
        self.width = width
        self.axis = axis
        self.direction = direction
        self.steps = steps

        if hat:
            self.hat = hat
        else:
            self.hat = PixelHat(auto_centre=True)

        self.populate()
        Path("renders/bands.pickle").write_bytes(pickle.dumps(self))

    def populate(self):
        """Populate ourself."""
        gap = 2 / (self.steps - 1)
        position = -1
        while position <= 1:
            upper_bound = position + self.width
            lower_bound = position - self.width
            filtered = filter(
                lambda w: lower_bound <= w[self.axis] <= upper_bound, self.hat
            )

            self.append(list(map(lambda w: w["index"], filtered)))

            position += gap


#     def render(self):
#         """Create the data."""
#         data = {}
#         for axis in ["x", "y", "z"]:
#             for direction in ["up", "down"]:
#                 key = f"{axis}_{direction}"
#                 data[key] = make_frames(self.hat, axis, direction)

#         Path("renders/bands.pickle").write_bytes(pickle.dumps(data))


# def make_frames(hat, axis, direction):
#     """Create some frames."""
#     steps = 100

#     rng = range(0 - steps, steps + 1, 1)
#     method = "less_than"

#     if direction == "down":
#         rng = range(steps, 0 - steps - 1, -1)
#         method = "greater_than"

#     data = []
#     for i in rng:
#         chunk = i / steps
#         data.append(list(filter(lambda x: getattr(x, method)(axis, chunk), hat)))

#     return data
