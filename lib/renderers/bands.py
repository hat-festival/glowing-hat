import pickle
from pathlib import Path
import numpy as np
from lib.pixel_hat import PixelHat


# THIS SHOULD WRITE JUST THE INDECES
class Band(list):
    """Individual Band sequence."""

    def __init__(self, width, count, axis, direction, hat=None):
        """Construct."""
        self.width = width
        self.count = count
        self.axis = axis
        self.direction = direction

        if hat:
            self.hat = hat
        else:
            self.hat = PixelHat(auto_centre=True)

        self.append([])

        for number in np.arange(-1, 2, 2 / (len(hat) - 1)):
            upper_bound = number
            lower_bound = number - self.width

            uppered = filter(lambda w: w[axis] <= upper_bound, self.hat)
            lowered = filter(lambda w: w[axis] > lower_bound, uppered)

            self.append(list(map(lambda w: w["index"], lowered)))

        self.append([])


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
