import pickle
from pathlib import Path


class Bands:
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat

    def render(self):
        """Create the data."""
        data = {}
        for axis in ["x", "y", "z"]:
            for direction in ["up", "down"]:
                key = f"{axis}_{direction}"
                data[key] = make_frames(self.hat, axis, direction)

        Path("renders/bands.pickle").write_bytes(pickle.dumps(data))


def make_frames(hat, axis, direction):
    """Create some frames."""
    steps = 100

    rng = range(0-steps, steps + 1, 1)
    method = "less_than"

    if direction == "down":
        rng = range(steps, 0-steps - 1, -1)
        method = "greater_than"

    data = []
    for i in rng:
        slice = i / steps
        data.append(list(filter(lambda x: getattr(x, method)(axis, slice), hat)))

    return data
