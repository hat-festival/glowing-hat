import pickle
from pathlib import Path

from lib.hat import Hat
from lib.tools import angle_to_point, remove_axis


class Sweeper:
    """Sweeper renderer."""

    def __init__(self, hat=None):
        """Construct."""
        if hat:
            self.hat = hat
        else:
            self.hat = Hat()

    def render(self):
        """Create some data."""
        data = {}
        for axis in ["x", "y", "z"]:
            axis_0, axis_1 = remove_axis(axis)

            for direction in ["f", "b"]:
                rev = False
                if direction == "b":
                    rev = True

                data[f"{axis}-{direction}"] = self.populate(axis_0, axis_1, rev=rev)

        Path("renders/sweeper.pickle").write_bytes(pickle.dumps(data))

    def populate(self, axis_0, axis_1, step=1, rev=False):  # noqa: FBT002
        """Populate ourself."""
        frames = []
        for angle in range(0, 360, step):
            frames.append(self.make_frame(axis_0, axis_1, angle, rev=rev))  # noqa: PERF401

        if not rev:
            frames.reverse()

        return frames

    def make_frame(self, axis_0, axis_1, offset, rev=False):  # noqa: FBT002
        """Make a single frame."""
        frame = []
        for pix in self.hat.pixels:
            point_angle = (angle_to_point(pix[axis_0], pix[axis_1]) + offset) % 360

            if rev:
                point_angle = 360 - point_angle

            if point_angle == 0:
                point_angle = 360

            factor = point_angle / 360

            frame.append((pix["index"], factor))

        return frame
